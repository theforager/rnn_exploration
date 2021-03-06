import torch

from torch import nn, einsum
from random import randint
from torch.nn import functional as f


class BasicRNN(nn.Module):
    ''' Basic RNN with a softmax output layer '''
    
    def __init__(self, input_size, hidden_size, output_size, output_length = 1):
        ''' Init the RNN '''
        super(BasicRNN, self).__init__()
        
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.output_length = output_length
        
        self.input_to_output = nn.Linear(input_size + hidden_size, output_size)
        self.input_to_hidden = nn.Linear(input_size + hidden_size, hidden_size)
        self.softmax = nn.LogSoftmax(dim=2)
        
    def forward(self, input, hidden):
        ''' Run a forward pass for a single input or sequence of inputs
        
        Args:
            input: single input or full sequence (size: seq_len, 1, input_size)
            hidden: simple hidden layer (size: 1, 1, hidden_size)
        
        Returns:
            full output sequence and very last hidden layer
        '''
        output = []
        
        for i in range(input.shape[0]):
            combined_input = torch.cat((input[i].unsqueeze(0), hidden), dim=2)
            hidden = self.input_to_hidden(combined_input)
            
        output.append(self.softmax(self.input_to_output(combined_input)))
        
        for j in range(1, self.output_length):
            combined_input = torch.cat((output[-1], hidden), dim=2)
            hidden = self.input_to_hidden(combined_input)
            output.append(self.softmax(self.input_to_output(combined_input)))
        
        output = torch.cat(output, dim=0)
        return output, hidden
    
    def init_hidden(self):
        ''' Returns new hidden layers for the start of a new sequence '''
        model_device = next(self.parameters()).device
        return torch.zeros(1, 1, self.hidden_size).to(model_device)
