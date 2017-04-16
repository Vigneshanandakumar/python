import re
import urllib2
import smtplib
import sched, time
import subprocess
import os
import sys

class BookMyShowClient(object):
  NOW_SHOWING_REGEX = '{"event":"productClick","ecommerce":{"currencyCode":"INR","click":{"actionField":{"list":"Filter Impression:category\\\/now showing"},"products":\[{"name":"(.*?)","id":"(.*?)","category":"(.*?)","variant":"(.*?)","position":(.*?),"dimension13":"(.*?)"}\]}}}'
  COMING_SOON_REGEX = '{"event":"productClick","ecommerce":{"currencyCode":"INR","click":{"actionField":{"list":"category\\\/coming soon"},"products":{"name":"(.*?)","id":"(.*?)","category":"(.*?)","variant":"(.*?)","position":(.*?),"dimension13":"(.*?)"}}}}'

  def __init__(self, location = 'Coimbatore'):
    self.__location = location.lower()
    self.__url = "https://in.bookmyshow.com/%s/movies" % self.__location
    self.__html = None

  def __download(self):
    req = urllib2.Request(self.__url, headers={'User-Agent' : "Magic Browser"})
    html = urllib2.urlopen(req).read()
    return html

  def get_now_showing(self):
    if not self.__html:
      self.__html = self.__download()
    now_showing = re.findall(self.NOW_SHOWING_REGEX, self.__html)
    return now_showing

  def get_coming_soon(self):
    if not self.__html:
      self.__html = self.__download()
    coming_soon = re.findall(self.COMING_SOON_REGEX, self.__html)
    return coming_soon


          
s = sched.scheduler(time.time, time.sleep)

if __name__ == '__main__':
  movies = ['Baahubali 2: The Conclusion','Bahubali 2: The Conclusion', 'Bahubali', 'Baahubali','Half Girlfriend']
  def sendemail_bms(names, link, email_content):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('from@gmail.com','password')
            msg="\r\n".join(["From:from@gmail.com","To:to@gmail.com","Subject:Bookings open for "+names,"",email_content])
            server.sendmail("from@gmail.com","to@gmail.com",msg)
            sys.exit("Email Sent")
        except:
            raise
          
  def check_movies(val):
    location = 'Coimbatore'
    bms_client = BookMyShowClient(location)
    now_showing = bms_client.get_now_showing()
    coming_soon = bms_client.get_coming_soon()
    movie_names = []
    content = []
    names =""
    links = ""
    email_content = ""
    for movie in now_showing:
      if movie[0] in movies:
        movie_name = movie[0]
        movie_names.append(movie_name)
        movie_name_lowc = movie[0].lower().replace(":","").replace(" ","-").replace(".","")
        movie_link = 'https://in.bookmyshow.com/'+location.lower()+'/movies/'+movie_name_lowc+'/'+movie[1]+'\n'
        content.append('\nTo book tickets for '+movie_name+' go to '+ movie_link)
        names =','.join(movie_names)
        links = ''.join(content)
        email_content = 'Bookings open for '+names+' at in.bookmyshow.com\n'+links
        
    if names:
      sendemail_bms(names, links, email_content)
    else:
      print "Bookings not open yet. Running routine again"
         
    s.enter(300, 1, check_movies, (s,))
  s.enter(300, 1, check_movies, (s,))
  s.run()
    
