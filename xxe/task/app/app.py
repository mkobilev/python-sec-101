from flask import Flask, request, render_template, send_file, session
from flask_session import Session
from lxml import etree
import uuid
from cachelib.file import FileSystemCache

app = Flask(__name__, template_folder='templates')
real_flag = ''

SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="./sessions"),
app.config.from_object(__name__)
Session(app)


with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return 'RIGHT!' if flag == real_flag else 'WRONG!'

xml_string = """
<!--?xml version="1.0" ?-->
<!DOCTYPE userCard [
                    <!ENTITY firstName "{firstName}">
                    <!ENTITY lastName "{lastName}">
                    <!ENTITY days "{days}">
                    ]>
<userInfo>
	<FIO>&firstName; &lastName;</FIO>
	<firstName>&firstName;</firstName>
	<lastName>&lastName;</lastName>
	<workDays>&days;</workDays>
    <totalSalary>TODO</totalSalary>
</userInfo>
"""

@app.route("/", methods=['POST', 'GET'])
def doLogin():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        days = request.form.get('days')
        xx = xml_string.format(firstName=firstName, lastName=lastName, days=days)        
        parser = etree.XMLParser(resolve_entities=True)
        tree = etree.fromstring(xx, parser)
        entity = etree.tostring(tree, pretty_print=True).decode('utf-8')
        
        ddid = uuid.uuid4()
        
        with open(f"./assets/{ddid}.xml", "w") as f:
            f.write(entity)
            
        # for row in tree:
        #     print(row.tag)
        #     print(row.text)
            
        session_id = session.get("key", "not set")
        print(session_id)

        return render_template('salary.html', salary_xml=entity, ddid=ddid)
        # return entity, {'Content-Type': 'text/xml;charset=UTF-8'}

    return render_template('index.html')


@app.route('/download/<uuid>', methods=['GET'])
def downloadFile(uuid: str):
    path = f"./assets/{uuid}.xml"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
