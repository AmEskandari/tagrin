import torch
from einops import rearrange
from torch import nn

from ..layers import BiGRIL
from ...utils.parser_utils import str_to_bool


class GRINet(nn.Module):
    def __init__(self,
                 adj,
                 d_in,
                 d_hidden,
                 d_ff,
                 ff_dropout,
                 n_layers=1,
                 kernel_size=2,
                 decoder_order=1,
                 global_att=False,
                 d_u=0,
                 d_emb=0,
                 layer_norm=False,
                 merge='mlp',
                 impute_only_holes=True,
                 window = 256,
                 num_heads = 3,
                 hidden_units = 256):
        super(GRINet, self).__init__()
        self.d_in = d_in
        self.d_hidden = d_hidden
        self.d_u = int(d_u) if d_u is not None else 0
        self.d_emb = int(d_emb) if d_emb is not None else 0
        self.register_buffer('adj', torch.tensor(adj).float())
        self.impute_only_holes = impute_only_holes

        self.bigrill = BiGRIL(input_size=self.d_in,
                              ff_size=d_ff,
                              ff_dropout=ff_dropout,
                              hidden_size=self.d_hidden,
                              embedding_size=self.d_emb,
                              n_nodes=self.adj.shape[0],
                              n_layers=n_layers,
                              kernel_size=kernel_size,
                              decoder_order=decoder_order,
                              global_att=global_att,
                              u_size=self.d_u,
                              layer_norm=layer_norm,
                              merge=merge)
        
        
        self.key = nn.Linear(window,hidden_units)
        self.query = nn.Linear(window,hidden_units)
        self.value = nn.Linear(window,hidden_units)
        
        self.att = nn.MultiheadAttention(hidden_units,num_heads = num_heads)
        
        
    def forward(self, x, mask=None, u=None, **kwargs):
    
        h = rearrange(x.squeeze(dim=3),'a b c -> c a b')
            
        k = self.key(h)
        q = self.query(h)
        v = self.value(h)
    
        _,adj = self.att(q, k, v)
    
        adj = torch.mean(adj, dim = 0)
        A = torch.where(self.adj > 0, adj, 0*torch.ones_like(adj))
        
        x = rearrange(x, 'b s n c -> b c n s')
        if mask is not None:
            mask = rearrange(mask, 'b s n c -> b c n s')

        if u is not None:
            u = rearrange(u, 'b s n c -> b c n s')

        imputation, prediction = self.bigrill(x, A, mask=mask, u=u, cached_support=self.training)

        if self.impute_only_holes and not self.training:
            imputation = torch.where(mask, x, imputation)
            
        imputation = torch.transpose(imputation, -3, -1)
        prediction = torch.transpose(prediction, -3, -1)
        if self.training:
            return imputation, prediction
        return imputation

    @staticmethod
    def add_model_specific_args(parser):
        parser.add_argument('--d-hidden', type=int, default=64)
        parser.add_argument('--d-ff', type=int, default=64)
        parser.add_argument('--ff-dropout', type=int, default=0.)
        parser.add_argument('--n-layers', type=int, default=1)
        parser.add_argument('--kernel-size', type=int, default=2)
        parser.add_argument('--decoder-order', type=int, default=1)
        parser.add_argument('--d-u', type=int, default=0)
        parser.add_argument('--d-emb', type=int, default=8)
        parser.add_argument('--layer-norm', type=str_to_bool, nargs='?', const=True, default=False)
        parser.add_argument('--global-att', type=str_to_bool, nargs='?', const=True, default=False)
        parser.add_argument('--merge', type=str, default='mlp')
        parser.add_argument('--impute-only-holes', type=str_to_bool, nargs='?', const=True, default=True)
        return parser
