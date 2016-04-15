from flask import Flask 
from flask import request 
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver 
 
browser = webdriver.Firefox() 
browser.implicitly_wait(5) # 5 seconds 
 
def get_results_for(text_to_classify): 
    browser.get('https://www3.wipo.int/ipccat/') 
    select = Select(browser.find_element_by_id("form1:nbOfPredictionDropDown_list")) 
    select.select_by_visible_text("5") 
     
    select = Select(browser.find_element_by_id("form1:classificationLevelDropDown_list")) 
    select.select_by_visible_text("Class") 
     
    input_area = browser.find_element_by_id("form1:pasteTextArea") 
    input_area.send_keys(text_to_classify) 
     
    browser.find_element_by_id("form1:classifyButton").click() 
     
    results_table = browser.find_element_by_id("form1:table1") 
    
    results_table = browser.find_element_by_id("form1:table1")
    stars_id = "form1:table1:tableRowGroup1:{row}:tableColumn1:image1"
    class_id = "form1:table1:tableRowGroup1:{row}:tableColumn2:staticText2"
    
    output = ""

    for i in xrange(5):
        stars_img = browser.find_element_by_id(stars_id.format(row=i))
        class_span = browser.find_element_by_id(class_id.format(row=i))
        output += class_span.text + " " + stars_img.get_attribute("src")[-5] + ","

    if output:
        output = output[:-1]

    return output

app = Flask(__name__)

@app.route("/get_results", methods=["GET"])

def get_results():
    try:
        text = request.args.get("text")
        results = ''
        with open('acc.log', 'a') as fl:
            fl.write('Request: ' + text + '\n')
            results = get_results_for(text)
            fl.write('Response: ' + str(results) + '\n')
        return results
    except:
        return "error"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) 
