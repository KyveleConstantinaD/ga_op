import pandas as pd
import os


def create_excel_file(avg_scores, avg_distances, scores, distances, routes_excel, t_list ,files, avg_gen, gen, cpu, avg_cpu, parent_cpu, aaa, test_run, tmax=None):    # Create a data frame with the data from lista and listb
    
    # create dataframe
    df = pd.DataFrame(t_list)
    df.insert(1, 'avg score', avg_scores)
    df.insert(2, 'avg distance', avg_distances)
    df.insert(3, 'avg generations', avg_gen)
    df.insert(4, 'best score', scores)
    df.insert(5, 'best distance', distances)
    df.insert(6, 'best route', routes_excel)
    df.insert(7, 'CPU', cpu)
    df.insert(8, 'avg CPU', avg_cpu)
    df.insert(9, 'CPU for parent selection', parent_cpu)
    df.insert(10, 'generations', gen)
    df.insert(11, 'best, first time found in gen', aaa)
    df.insert(12, 'test run', test_run)
    
    # set name for file
    name_after_tests = os.path.relpath(files, 'Sets')
    name_without_extension = os.path.splitext(name_after_tests)[0]

    # Save the data frame to an Excel file
    excel_file = str(name_without_extension)+'_'+str(tmax)+'_output.xlsx'
    print('excel output generated')
    
    # generate excel file
    df.to_excel(excel_file, index=False)

if __name__ == "__main__":

    create_excel_file(lista, listb)
