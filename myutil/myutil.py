import os, sys, time, datetime,inspect, json


def git_repo_root():
    cmd = "git rev-parse --show-toplevel"
    mout, merr = os_system(cmd)
    path = mout.split("\n")[0]
    if len(path) < 1:
        return None
    else 
        return path

    
class dict_to_namespace(object):
    def __init__(self, d):
        self.__dict__ = d

def os_get_function_name():
    return sys._getframe(1).f_code.co_name


def os_getcwd():
    root = os.path.abspath(os.getcwd()).replace("\\", "/") + "/"
    return  root

def os_system(cmd, doprint=False):
  """ get values
       os_system( f"   ztmp ",  doprint=True)
  """
  import subprocess  
  try :
    p          = subprocess.run( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, )
    mout, merr = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')    
    if doprint: 
      l = mout  if len(merr) < 1 else mout + "\n\nbash_error:\n" + merr
      print(l)

    return mout, merr
  except Exception as e :
    print( f"Error {cmd}, {e}")

    
def verbosity_get(cur_path, path_relative="/../../config.json",
                   default=5, key='verbosity',):
    """
    verbosity = verbosity_get(__file__, "/../../config.json", default=5 )
    :param cur_path:
    :param path_relative:
    :param key:
    :param default:
    :return:
    """
    try   :
      verbosity = int(json.load(open(os.path.dirname(os.path.abspath(cur_path)) + path_relative , mode='r'))[key])
    except Exception as e :
      verbosity = default
      #raise Exception(f"{e}")
    return verbosity

  
def os_makedirs(dir_or_file):
    if os.path.isfile(dir_or_file) :
        os.makedirs(os.path.dirname(os.path.abspath(dir_or_file)), exist_ok=True)
    else :
        os.makedirs(os.path.abspath(dir_or_file), exist_ok=True)


class Session(object) :
    """ Save Python session on disk
      from util import Session
      sess = Session("recsys")
      sess.save( globals() )
    """
    def __init__(self, dir_session="ztmp/session/",) :
      os.makedirs(dir_session, exist_ok=True)
      self.dir_session =  dir_session
      self.cur_session =  None
      print(self.dir_session)

    def show(self) :
       import glob
       flist = glob.glob(self.dir_session + "/*" )
       print(flist)

    def save(self, name, glob=None, tag="") :
       path = f"{self.dir_session}/{name}{tag}/"
       self.cur_session = path
       os.makedirs(self.cur_session, exist_ok=True)
       save_session(self.cur_session, glob)

    def load(self, name, glob:dict=None, tag="") :
      path = f"{self.dir_session}/{name}{tag}/"
      self.cur_session = path
      print(self.cur_session)
      load_session(self.cur_session , glob )


def save_session(folder , globs, tag="" ) : 
  import pandas as pd
  os.makedirs( folder , exist_ok= True)   
  lcheck = [ "<class 'pandas.core.frame.DataFrame'>", "<class 'list'>", "<class 'dict'>",
             "<class 'str'>" ,  "<class 'numpy.ndarray'>" ]  
  lexclude = {   "In", "Out" }
  gitems = globs.items()
  for x, _ in gitems :
     if not x.startswith('_') and  x not in lexclude  :
        x_type =  str(type(globs.get(x) ))
        fname  =  folder  + "/" + x + ".pkl"
        try :       
          if "pandas.core.frame.DataFrame" in x_type :
              pd.to_pickle( globs[x], fname)
        
          elif x_type in lcheck or x.startswith('clf')  :
              save( globs[x], fname ) 
              
          print(fname)    
        except Exception as e:
              print(x, x_type, e)


def load_session(folder, globs=None) :
  """
  """
  print(folder)
  for dirpath, subdirs, files in os.walk( folder ):
    for x in files:
       filename = os.path.join(dirpath, x) 
       x = x.replace(".pkl", "")
       try :
         globs[x] = load(  filename )
         print(filename) 
       except Exception as e :
         print(filename, e)


def save(dd, to_file="", verbose=False):
  import pickle, os
  os.makedirs(os.path.dirname(to_file), exist_ok=True)
  pickle.dump(dd, open(to_file, mode="wb") , protocol=pickle.HIGHEST_PROTOCOL)
  #if verbose : os_file_check(to_file)


def load(to_file=""):
  import pickle  
  dd =   pickle.load(open(to_file, mode="rb"))
  return dd



##################################################################################################
def test():
   pass

  
if __name__ == "__main__":
    import fire
    fire.Fire()






      
