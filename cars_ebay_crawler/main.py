from re import M
from webbrowser import MacOSX
from pip import main
from ebay_cars import get_data, parse,output
from check_last_cars import lastAdded
from multiprocessing import Process

carList = {
    "Ford", "Chevorlet" , "cadillac", "Nissan", "Toyota", "Tesla", "Jeep", "Kia", "GMC", "Subaru", "BMW"
}

# for car in carList:
def parse_by_car(car):
    searchterm = car
    lastupdated = lastAdded(car +"_output")
    soup = get_data(searchterm)
    productslist = parse(soup,lastupdated)
    output(productslist, searchterm, lastupdated)

def run_parallel(*functions):
    '''
    Run functions in parallel
    '''
    from multiprocessing import Process
    processes = []
    for function in functions:
        proc = Process(target=function)
        proc.start()
        processes.append(proc)
    for proc in processes:
        proc.join()

if __name__ == "__main__":
    run_parallel(parse_by_car("Kia"), parse_by_car("cadillac"))


