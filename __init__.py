from presentations.PresentationTopics import Topic, Slide
from custompackages import declarePersonalPackage

declarePersonalPackage(__file__, __package__ if __package__ else 'presentations')
Topic = Topic
Slide = Slide
