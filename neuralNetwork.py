from pyrosim.neuron  import NEURON
import math

from pyrosim.synapse import SYNAPSE

class NEURAL_NETWORK: 

    def __init__(self,nndfFileName):

        self.neurons = {}

        self.synapses = {}

        f = open(nndfFileName,"r")

        for line in f.readlines():

            self.Digest(line)

        f.close()

    def Print(self):

        self.Print_Sensor_Neuron_Values()

        self.Print_Hidden_Neuron_Values()

        self.Print_Motor_Neuron_Values()

        print("")

# ---------------- Private methods --------------------------------------

    def Update(self):
        # 1) Update sensor neurons from touch sensors
        for neuronName in self.neurons:
            if self.neurons[neuronName].Is_Sensor_Neuron():
                self.neurons[neuronName].Update_Sensor_Neuron()

        # 2) Update all non-sensor neurons (motor + hidden) from incoming synapses
        for targetName in self.neurons:
            if not self.neurons[targetName].Is_Sensor_Neuron():
                total = 0.0
                for sourceName in self.neurons:
                    key = (sourceName, targetName)
                    if key in self.synapses:
                        total += self.synapses[key].Get_Weight() * self.neurons[sourceName].Get_Value()
                val = math.tanh(total)
                # Some versions have Set_Value, some just store .value
                try:
                    self.neurons[targetName].Set_Value(val)
                except AttributeError:
                    self.neurons[targetName].value = val
    def Add_Neuron_According_To(self,line):

        neuron = NEURON(line)

        self.neurons[ neuron.Get_Name() ] = neuron

    def Add_Synapse_According_To(self,line):

        synapse = SYNAPSE(line)

        sourceNeuronName = synapse.Get_Source_Neuron_Name()

        targetNeuronName = synapse.Get_Target_Neuron_Name()

        self.synapses[sourceNeuronName , targetNeuronName] = synapse

    def Digest(self,line):

        if self.Line_Contains_Neuron_Definition(line):

            self.Add_Neuron_According_To(line)

        if self.Line_Contains_Synapse_Definition(line):

            self.Add_Synapse_According_To(line)

    def Line_Contains_Neuron_Definition(self,line):

        return "neuron" in line

    def Line_Contains_Synapse_Definition(self,line):

        return "synapse" in line

    def Print_Sensor_Neuron_Values(self):

        print("sensor neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Sensor_Neuron():

                self.neurons[neuronName].Print()

        print("")

    def Print_Hidden_Neuron_Values(self):

        print("hidden neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Hidden_Neuron():

                self.neurons[neuronName].Print()

        print("")

    def Print_Motor_Neuron_Values(self):

        print("motor neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Motor_Neuron():

                self.neurons[neuronName].Print()

        print("")
