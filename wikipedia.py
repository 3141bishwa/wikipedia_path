# coding=utf-8

from bs4 import BeautifulSoup
import requests
import re

#defining a single wikipedia page
class vertex(object):

    # Parameters:
    # link : the full link to the wikipedia page
    # parent : the vertex object whose link led to the current page
    # Note : Although many pages can lead to the same page,
    # for the purposes of this code, we consider the page which led to
    # the current page during the graph traversal as the parent page
    # The parent to the starting vertex is kept as None
    def __init__(self,link, parent):
        self.link = link
        self.parent = parent

    # scrapes the HTML of a wikipedia page and returns all vertex objects
    # which can lead to other wikipedia pages
    def getNeighbours(self):
        response = requests.get(self.link)
        response =  response.content
        soup = BeautifulSoup(response, 'html.parser')
        myDiv = soup.find(id="mw-content-text")
        soup = BeautifulSoup(str(myDiv), 'html.parser')
        myList = soup.find_all(title=True, href=re.compile("^/wiki/"))
        
        if myList is None:
          return None

        myWikipediaList = []
        
        for x in myList:
          myString = str(x.get('href'))
          if myString[6:11] =="File:" or myString[6:14] =="Special:" or myString[6:15]=="Template:":
            pass
          else:
              myWikipediaList.append(vertex('https://en.wikipedia.org'+ myString,self))
        return myWikipediaList
        
    # Gives the shortest path for the current vertex to the vertex at the start    
    def get_shortest_path(self):
      shortest_path = []
      current = self
      while current!= None:
        shortest_path.append(current.link)
        current = current.parent
      return shortest_path[::-1]  

# Returns the route between the two wikipedia pages
def getRoute(initial,final):
  
  initialVertex = vertex(initial, None)
  
  if(initial ==final):
    return "same webpage"
  
  #sets the level of the initial vertex as 0  
  level= {initialVertex:0}

  frontier = [initialVertex]
  
  #sets the 
  i = 1

  #loops through the frontier list until it's not empty
  while frontier:
    start = frontier.pop(0)
    for neighbours in start.getNeighbours():
      print neighbours.link
      if neighbours.link == final:
        return  neighbours.get_shortest_path()
      elif neighbours.link not in level:
        level[i] = neighbours.link
        frontier.append(neighbours)
    i+=1
  return None

print getRoute("https://en.wikipedia.org/wiki/Pakistan", "https://en.wikipedia.org/wiki/Kolkata")

