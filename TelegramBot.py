import os
import telebot
import psutil

API_KEY = os.environ['API_KEY']   
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, "*Welcome to my telegram bot!*",parse_mode= 'Markdown');

@bot.message_handler(commands=['Memory_usage'])
def mem(message):
  values = psutil.virtual_memory()
  str1 = "Total memory :" + str(values.total>>30) + " GB"
  str2 = "Memory used :" + str(values.available>>30) + " GB"
  bot.reply_to(message, str1+"\n"+str2)


def getListOfProcessSortedByMemory():

  listOfProcObjects = []
  # Iterate over the list
  for proc in psutil.process_iter():
      try:
          # Fetch process details as dict
          pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
          pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
          # Append dict to list
          listOfProcObjects.append(pinfo);
      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
          pass
  # Sort list of dict by key vms i.e. memory usage
  listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
  
  return listOfProcObjects

@bot.message_handler(commands=['Running_processes'])
def process_check(message):
  str3=""
  listOfRunningProcess = getListOfProcessSortedByMemory()
  for elem in listOfRunningProcess[:5] :
    str3 = str3 + "\n"+str(elem.get('name'))
  
  bot.send_message(message.chat.id, "Top 5 process by memory usage:\n"+str3)

  @bot.message_handler(commands=['battery'])
  def battery(message):
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    plugged = "Plugged In" if plugged else "Not Plugged In"
    str4 = percent+'% | '+plugged
    bot.send_message(message.chat.id, "Battery Status: "+str4)

  @bot.message_handler(commands=['cpu_usage'])
  def cpu_usage(message):
    usage = str(psutil.cpu_percent(60)) #cpu usage in the last 1 min
    bot.send_message(message.chat.id, "CPU usage in the last 1 minute: "+usage+"%")
  
  @bot.message_handler(commands=['disk_usage'])
  def disk_usage(message):
    usage1 = psutil.disk_usage('/')
    ttl = str(usage1.total>>30)+" GB"
    fr = str(usage1.free>>30)+" GB"
    bot.send_message(message.chat.id, "*Disk usage:*\nTotal: "+ttl+"\nAvailable: "+fr,parse_mode= 'Markdown')


bot.polling()
 