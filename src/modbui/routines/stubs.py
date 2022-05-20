import xml.etree.ElementTree as ET

#these points define a closed shape of the outer contour
test_shape = [(0,0),
              (200,0),
              (200,600),
              (0,600),
              (0,0)]



##Calculating layup shape stubs from given xml

tree = ET.parse('Model-1.xml')

def extract_lines(layer_num):
    '''

    :param layer_num:
    :return: list of lines
    '''

    layer_num -= 1

    exte = tree.find('layout_output_data').find('layers').findall('layer')[layer_num].find('exterior_points').findall(
        'point')
    base = tree.find('layout_output_data').find('layers').findall('layer')[layer_num].find('base_points').findall(
        'point')



    x_base = [float(i.get('x')) for i in base] #list of x coordinates of the points in the base line
    y_base = [float(i.get('y')) for i in base]
    x_exte = [float(i.get('x')) for i in exte]
    y_exte = [float(i.get('y')) for i in exte]

    base_line = tuple(zip(x_base, y_base))
    external_line = tuple(zip(x_exte, y_exte))


    return base_line, external_line


liner = tree.find('layout_output_data').find('liner_modified').findall('point')
x_liner = [float(i.get('x')) for i in liner]
y_liner = [float(i.get('y')) for i in liner]
liner_curve = tuple(zip(x_liner, y_liner))

##collecting lines
num_layers = 40

test_lines = []
test_lines.append(liner_curve)
for layer in range(1, num_layers+1):
    base, exte = extract_lines(layer)
    # test_lines.append(base)
    test_lines.append(exte)

test_lines = tuple(test_lines)
