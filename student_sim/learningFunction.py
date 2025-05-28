import numpy as np

class sigmoidLearningFunction():
  def __init__(self, a=0.1, b=0.5):
    """
    Initialize the sigmoid learning function.
    
    Parameters:
    a (float): Parameter that affects the steepness of the curve.
    b (float): Parameter that shifts the curve horizontally.
    """
    self.a = a
    self.b = b
    self.origin = self.get_time_0()
  
  def get_time_0(self):
    """
    Calculate the time at which the probability of success is 0.
    
    Parameters:
    a (float): Parameter that affects the steepness of the curve.
    b (float): Parameter that shifts the curve horizontally.
    
    Returns:
    float: The time at which the probability of success is 0.
    """
    last_number = 100 
    
    for i in range(-100, 100):
      if self.__call__(i) <= 1e-2:
        last_number = i
      if self.__call__(i) > 1e-2:
        return last_number
    
    
  def __call__(self, time):
    """
    Calculate the probability of success at a given time using a sigmoid function.
    Parameters:
    time (int): The time spent learning.
    Returns:
    float: The probability of success at the given time.
    """
    return 1 / (1 + np.exp(-self.a * (time - self.b)))




class learningFunction():
    """
    Base class for learning functions.
    """

    def __init__(self, func):
        self.func = func

    def __str__(self) -> str:
        return f"LearningFunctionBase(func={self.func})"
    def __repr__(self) -> str:
        return self.__str__()
    
    def learn(self, prob_guess, prob_slip, time):
      """
      Simulate the learning process.
      
      Parameters:
      prob_guess (float): Probability of guessing correctly.
      prob_slip (float): Probability of slipping (making a mistake).
      time (int): Time spent learning.
      
      Returns:
      float: Effectiveness of the learning process.
      """
      # *np.exp(-(time-self.func.origin)/25)
      prob_acierto = self.func(time)
      prob_acierto_completo = prob_acierto*(1-prob_slip) + prob_guess*(1-prob_acierto)
      return prob_acierto_completo
    
    
    def __call__(self, prob_guess, prob_slip, time):
        """
        Call the learning function with the given parameters.
        Parameters:
        prob_guess (float): Probability of guessing correctly.
        prob_slip (float): Probability of slipping (making a mistake).
        time (int): Time spent learning.
        Returns:
        float: Effectiveness of the learning process.
        """
        return self.learn(prob_guess, prob_slip, time)
      
