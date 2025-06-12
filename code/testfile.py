'''

Testfile which runs evaluation.py a certain number of times.

'''
import subprocess

# setting up all our possibilities for each argument provided to
# evaluation.py.
program = "./code/evaluation.py"
collection = "CISI_simplified"
scoring_schemes = ['ltn', 'lnn', 'nnn', 'ntn', 'ltc', 'lnc', 'nnc', 'ntc']
methods = ['l', 's']
metrics = ['mrr', 'map']

def repeat_funct(run_number):
    
    # writing our outputs into files (mainly to avoid the ntlk printing).
    file_name = "sample" + run_number + ".txt"
    file = open(file_name, 'w')

    # retrieving documents [10, 860, 1710] with query.py.
    for k in [10, 860, 1710]:
        
        # randomly selecting [10, 80] queries with evaluation.py. 
        for r in [10, 80]:
            
            print("documents: " + str(k) + " queries: " + str(r), file = file)

            # selecting a scoring scheme from ['ltn', 'lnn', 'nnn', 'ntn', 'ltc', 'lnc', 'nnc', 'ntc'].
            for scheme in scoring_schemes:
                
                # selecting a method from ['l', 's'].
                for method in methods:
                    
                    # selecting a metric from ['mrr', 'map'].
                    for metric in metrics:
                        output = subprocess.check_output(["python3", program, collection, scheme, method, str(k), str(r), metric])
                        output = output.decode('utf-8').strip()
                        file.write(output)
                        file.write('\n')
                    
                    print("-" * 100, file=file)
        file.write('\n')
    file.close()

if __name__ == "__main__":
    # running this scoring twice.
    # NOTE: this program takes roughly 3-4 hours.
    for i in range(2):
        temp = i + 1
        repeat_funct(str(temp))
