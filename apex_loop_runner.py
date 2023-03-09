# @author Liquad Li
# @date 2022-10

'''
This script is written in Python and uses the simple_salesforce library to connect to Salesforce and execute Apex code using the Salesforce Tooling API. 
The script reads a list of IDs from a file and batches them into groups of five. For each batch, it replaces a placeholder string in a template Apex script with the IDs 
in the batch and executes the resulting Apex code using the exec_anon function. If the execution is successful, it moves on to the next batch, otherwise it stops.

The script uses the following functions:

createConn(): This function reads a JSON file containing Salesforce login credentials and returns a Salesforce object that can be used to connect to Salesforce.
changeScript(idlist): This function reads a template Apex script from a file, replaces a placeholder string with a comma-separated list of IDs, and returns the updated
Apex script.
exec_anon(self, apex_string): This function executes a string of Apex code using the Salesforce Tooling API. It returns True if the execution was successful and False 
otherwise.
print_hi(name): This function is the main function of the script. It connects to Salesforce using createConn(), reads a list of IDs from a file, batches them into groups
of five, replaces a placeholder string in a template Apex script with the IDs in the batch using changeScript(), and executes the resulting Apex code using exec_anon().
If the execution is successful, it moves on to the next batch, otherwise it stops.
'''


import json
import os
from collections import OrderedDict

from simple_salesforce import Salesforce, SFType, SalesforceLogin, format_soql, SalesforceGeneralError

def exec_anon(self, apex_string):
        """Executes a string of Apex code.
        """
        url = self.tooling_url + "executeAnonymous/"
        params = {'anonymousBody': apex_string}
        result = self._call_salesforce('GET', url, headers=self.headers, params=params)

        if result.status_code != 200:
            raise SalesforceGeneralError(url,
                                         'executeAnonymous',
                                         result.status_code,
                                         result.content)
        json_result = result.json(object_pairs_hook=OrderedDict)
        if len(json_result) == 0:
            print('Execute with no result.')
            return None
        if json_result['compiled'] == True and json_result['success'] == True:
            print('Execute successfully.')
            return True
        else:
            print('Execute failed.')
            print(json_result)
            return False

def createConn():
    with open(r"C:\Users\liquad\PycharmProjects\pythonProject\venv\login_SF.json", "r") as login_file:
        creds = json.load(login_file)

    sf = Salesforce(username=creds['login']['username'],
                    password=creds['login']['password'],
                    security_token=creds['login']['token'],
                    instance_url=creds['login']['instance_url'],
                    organizationId=creds['login']['organizationId'],
                    domain=creds['login']['domain'])
    return sf

def changeScript(idlist):
    with open(r"C:\Users\liquad\PycharmProjects\pythonProject\venv\script_template.txt", "r") as script_file:
        lines = script_file.read()
        updatedlines = lines.replace("$(ID_LIST)", idlist)
        #print(updatedlines)

    return updatedlines


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    sf = createConn()

    batchsize = 5
    curBatch = 0
    with open(r"C:\Users\liquad\PycharmProjects\pythonProject\venv\ids.txt", "r") as ids_file:
        lines = ids_file.readlines()
        maxline = len(lines)
        print(maxline)
        while curBatch <= maxline:
            print('curBatch: ')
            print(curBatch)
            idlist = ''
            idx = 0
            while idx < batchsize:
                if idx + curBatch >= maxline:
                    break
                #print(idx + curBatch)
                aline = lines[idx + curBatch]
                alineArray = aline.split('|')
                aid = alineArray[len(alineArray) - 1]
                aid = aid.removesuffix('\n')
                #print(len(aid))
                #print(aid)
                idlist += ",'" + aid + "'"
                idx += 1
            print(idlist.removeprefix(","))
            updatedScriptBody = changeScript(idlist.removeprefix(","))
            #runApex()
            if False == exec_anon(sf, updatedScriptBody):
                break
            curBatch += batchsize

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')



