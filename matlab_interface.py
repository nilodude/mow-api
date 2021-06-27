from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

import os
from io import StringIO

global import_fail
try:  # Check if the Matlab Engine is installed
    import matlab.engine
    from matlab.engine import RejectedExecutionError as MatlabTerminated
except ImportError:
    print("Matlab Engine for Python cannot be detected. Please install it for the extension to work")
    import_fail = True
else:
    import_fail = False


class MatlabInterface:
    global import_fail

    def __init__(self):
        # OS checks related work
        if os.name == 'nt':
            self.cls_str = 'cls'
        else:
            self.cls_str = 'clear'
        # self.clear()
        if not import_fail:
            print("Starting Matlab...")
            self.eng = matlab.engine.start_matlab()
            # future = matlab.engine.start_matlab(background=True)
            # self.eng = future.result()
        else:
            print("Could not start Matlab")

    def stop(self):
        print("stopping Matlab...")
        self.eng.quit()
        return "stopped OK"

    def clear(self):
        os.system(self.cls_str)

    def run_script(self, script_path):
        if not import_fail:
            try:
                print("Running Script: {}".format(script_path))
                stream = StringIO()
                err_stream = StringIO()
                self.eng.run(script_path, nargout=0,
                             stdout=stream, stderr=err_stream)
                return stream.getvalue().replace('\n', '')
            except MatlabTerminated:
                print(stream.getvalue(), err_stream.getvalue(), sep="\n")
                print("Matlab terminated. Restarting the engine...")
                self.eng = matlab.engine.start_matlab()
                self.eng.eval('cd \'D:\\Dropbox\\tfg\\Shazam-MATLAB\\app\\\'', nargout=0,
                              stdout=stream, stderr=err_stream)
                return "Matlab restarted OK"
            except:  # The other exceptions are handled by Matlab
                errList = err_stream.getvalue().split('\n\n')
                newList = [error.replace('\n', '') for error in errList]
                return list(filter(None, newList))

    def run_command(self, command, verbose):
        if not import_fail:
            try:
                if verbose:
                    print("Running Command: {}".format(command))
                stream = StringIO()
                err_stream = StringIO()
                self.eng.eval(command, nargout=0,
                              stdout=stream, stderr=err_stream)
                return stream.getvalue().replace('ans =', '').strip()
            except MatlabTerminated:
                print(stream.getvalue(), err_stream.getvalue(), sep="\n")
                print("Matlab terminated. Restarting the engine...")
                self.eng = matlab.engine.start_matlab()
                self.eng.eval('cd \'D:\\Dropbox\\tfg\\Shazam-MATLAB\\app\\\'', nargout=0,
                              stdout=stream, stderr=err_stream)
                return "Matlab restarted OK"
            except:  # The other exceptions are handled by Matlab
                # return (stream.getvalue() + "\n" + err_stream.getvalue() + "\n")
                errList = err_stream.getvalue().split('\n\n')
                newList = [error.replace('\n', '') for error in errList]
                return list(filter(None, newList))

    def run_selection(self, temp_path):
        if not import_fail:
            f = open(temp_path, 'r')
            print("Running:")
            try:  # Print the content of the selection before running it, encoding issues can happen
                for line in f:
                    print(line, end='')
            except UnicodeDecodeError:
                print("current selection")
            print('\n')
            f.close()
            try:
                stream = StringIO()
                err_stream = StringIO()
                self.eng.run(temp_path, nargout=0,
                             stdout=stream, stderr=err_stream)
                print(stream.getvalue())
            except MatlabTerminated:
                print(stream.getvalue(), err_stream.getvalue(), sep="\n")
                print("Matlab terminated. Restarting the engine...")
                self.eng = matlab.engine.start_matlab()
                print("Matlab restarted")
            except:  # The other exceptions are handled by Matlab
                print(stream.getvalue(), err_stream.getvalue(), sep="\n")
            finally:
                os.remove(temp_path)
                os.rmdir(os.path.dirname(temp_path))

    def interactive_loop(self):
        loop = True  # Looping allows for an interactive terminal
        while loop and not import_fail:
            print('>> ', end='')
            command = input()
            if command == "exit" or command == "exit()":  # Keywords to leave the engine
                loop = False
            elif command == "clc":  # matlab terminal clearing must be reimplemented
                self.clear()
            else:
                try:
                    stream = StringIO()
                    err_stream = StringIO()
                    # Feed the instructions to Matlab eval
                    self.eng.eval(command, nargout=0,
                                  stdout=stream, stderr=err_stream)
                    print(stream.getvalue())
                except MatlabTerminated:
                    print(stream.getvalue(), err_stream.getvalue(), sep="\n")
                    print("Matlab terminated. Restarting the engine...")
                    self.eng = matlab.engine.start_matlab()
                    print("Matlab restarted")
                except:  # The other exceptions are handled by Matlab
                    print(stream.getvalue(), err_stream.getvalue(), sep="\n")
        if not import_fail:
            self.eng.quit()
