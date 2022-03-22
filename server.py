from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET

server = SimpleXMLRPCServer(('localhost', 9000))


def save_data(topic, title, text, timestamp):
    print("The save function was called")
    
    # read data from db.xml and get the root

    tree = ET.parse('db.xml')
    root = tree.getroot()

    try:
        # Check if the topic is on database already

        input_topic = root.find("topic[@name='" + topic + "']")
        if input_topic is not None:
            new_note = ET.SubElement(input_topic, "note", name=title)   # New note for found topic
            ET.SubElement(new_note, "text").text = text 
            ET.SubElement(new_note, "timestamp").text = timestamp
        
        else:
            new_topic = ET.SubElement(root, "topic", name=topic)  # Topic was not found so new topic is added under root
            new_note = ET.SubElement(new_topic, "note", name=title)
            ET.SubElement(new_note, "text").text = text
            ET.SubElement(new_note, "timestamp").text = timestamp
   
    except:
        print("There was an error saving the data")
        return False

    tree.write('db.xml')
    return 'Data was saved to the database\n'


def read_data(topic):
    print("The read function was called")
    
    # Read data from db.xml and get the root   
    tree = ET.parse('db.xml')
    root = tree.getroot()
    data = []

    try:
        # Find the topic element given and return it
        element = root.find("topic[@name='" + topic + "']")
        print(ET.tostring(element))
        
        if element is not None:
            notes = element.findall("note")
            # Get data from each note, append to list and finally return the list
            
            for note in notes:
                title = note.get('name')
                text = note.find("text").text
                timestamp = note.find("timestamp").text
                data.append(f'Title: {title}\n'
                            f'Note: {text}\n'
                            f'Timestamp {timestamp}')
            return data
        
        else:
            return False
    
    except:
        # Topic was not found
        print('There was an error while trying to read the data')
        return False


# Register the functions and start server
server.register_function(save_data, 'save')
server.register_function(read_data, 'read')
print("Server listening at port 9000...")
server.serve_forever()