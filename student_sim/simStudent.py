from student_sim.skill import Skill
from typing import List
import numpy as np
from typing import Dict
# Import BaseModel
from pydantic import BaseModel



class DataEntry(BaseModel):
    order_id: int
    user_id: str
    skill_name: str
    correct: int
    item_id: str
    subject_id: str

class Student():
  def __init__(self, user_id, learning_func, prob_slip=0.1):
    self.user_id = user_id
    self.learning_func = learning_func
    self.prob_slip = prob_slip
    self.ntries = 0
    self.learning_history : List[DataEntry] = []
    
  def __str__(self):
    return f"Student(user_id={self.user_id}, learning_func={self.learning_func})"
  
  def __repr__(self):
    return self.__str__()
  
  def learn(self, skill : Skill, time :  int):
    """
    Simulate the learning process of a student.
    
    Parameters:
    skill (Skill): The skill to be learned.
    time (int): The time spent learning the skill.
    
    Returns:
    float: The effectiveness of the learning process.
    """
    start_time = self.learning_func.func.origin
    for t in range(start_time, time + start_time):
      t_i = t /20
      prob_correct = self.learning_func(skill.prob_guess, self.prob_slip, t_i)
      correct = np.random.binomial(1, prob_correct)
      self.ntries += 1
      data_entry = DataEntry(
          order_id=self.ntries,
          user_id=self.user_id,
          skill_name=skill.skill_name,
          correct=correct,
          item_id=f"{self.user_id}_{skill.skill_name}_{self.ntries}",
          subject_id=skill.subject
      )
      self.learning_history.append(data_entry)
    return self.learning_history
    