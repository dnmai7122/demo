import torch
import torch.nn as nn


class LSTMClassifier(nn.Module):
    def __init__(self, input_size=144, hidden_size=128, num_layers=2, num_classes=5):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.2,
        )
        self.layernorm = nn.LayerNorm(hidden_size * 2)
        self.attn = nn.Linear(hidden_size * 2, 1)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_size * 2, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)                         # (B, T, 2H)
        out = self.layernorm(out)                    # (B, T, 2H)
        attn_weights = torch.softmax(self.attn(out), dim=1)  # (B, T, 1)
        out = (attn_weights * out).sum(dim=1)        # (B, 2H)
        out = self.dropout(out)
        return self.fc(out)                          # (B, num_classes)


def load_model(
    model_path: str,
    device: str = "cpu",
    input_size: int = 144,
    hidden_size: int = 128,
    num_layers: int = 2,
    num_classes: int = 5,
) -> LSTMClassifier:
    model = LSTMClassifier(
        input_size=input_size,
        hidden_size=hidden_size,
        num_layers=num_layers,
        num_classes=num_classes,
    )
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)  # strict=True (mặc định) để khớp 100%
    model.to(device)
    model.eval()
    return model
