# skill.py
import numpy as np


class Skill():
  
  def __init__(self, skill_name, subject, prob_guess):
    self.skill_name = skill_name
    self.subject = subject
    self.prob_guess = prob_guess
    
  def __str__(self):
    return f"Skill(skill_name={self.skill_name}, prob_guess={self.prob_guess}, prob_slip={self.prob_slip})"
  
  def __repr__(self):
    return self.__str__()