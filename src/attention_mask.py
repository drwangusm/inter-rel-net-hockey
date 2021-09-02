import torch
import torch.nn as nn
class SelfAttention(nn.Module):

    """
    https://arxiv.org/pdf/1703.03130.pdf

    """

    def __init__(
        self,
        input_size: int,
        num_outputs: int = 1,
        num_head: int = 1,
        projection_size=None,
    ):
        super().__init__()

        if projection_size is None:
            projection_size = input_size

        self.num_outputs = num_outputs
        self.num_head = num_head
        self.u_it = nn.Linear(input_size, projection_size, bias=False)
        self.Tanh = nn.Tanh()
        self.context = nn.Linear(projection_size, num_outputs * num_head, bias=False)

    @staticmethod
    def exp_normalize(x, mask):
        # Subtracting a constant in the exponent doesn't change the probability distribution
        # of the softmax. e**-b gets canceled out in the numerator and denominator.
        b = x.max()
        y = torch.exp(x - b)

        # Applying the mask after the exp() has the effect of nullifying
        # the masked positions. They will not count in the sum when normalizing
        if mask is not None:
            y = y * mask.unsqueeze(-1)

        # Adding a small constant to the normalizing factor in case everything
        # is zero
        return y / (
            y.unsqueeze(1).sum(dim=2) + 1.2e-38
        )  # 1.175494e-38  is smallest float32 value

    # pylint: disable=arguments-differ
    def forward(self, x, mask=None):
        """
        N: Batch Size
        W: Sequence length
        I: Input size
        O: Output size (num outputs)
        H: num_head

        Parameters
        ----------

        x: torch.tensor
            Tensor of shape (W, N, I) or (N, W, I) if batch_first

        mask: torch.tensor (optional)
            If provided, must be filled with 0 and 1. The position with 1
            are NOT masked. The positions with 0 will be masked.

        Returns
        -------
        Tuple[torch.tensor, torch.tensor]
            First item is the sentence embedding aggregated from a weighted
            average of the token embeddings
            Second item is the attention used for the weighted average
        """

        N = x.shape[0]

        # (N, W, I) -> (N, W, I)
        u_it = self.Tanh(self.u_it(x))
        # (N, W, I) -> (N, W, H*O)
        context = self.context(u_it)
        # Second dimension, W, will sum to one
        # (N, W, H*O)/(N, 1, W, H*O).sum(dim=2) -> (N, 1, W, H*O)
        attention = self.exp_normalize(context, mask)

        # (N, W, I) -> (N, I, W)
        x = x.transpose(1, 2)
        # Weighted average of the input vectors
        # (N, I, W)*(N, W, O*H) = (N, I, H*O)
        sentence = torch.matmul(x, attention)

        # (N, I, O*H) -> (N, I*H, O)
        return (
            sentence.view(N, -1, self.num_outputs),
            attention.view(N, -1, self.num_head, self.num_outputs),
        )
