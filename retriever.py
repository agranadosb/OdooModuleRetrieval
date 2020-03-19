# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
import queue


class Retriever():
    """
    Has methods for get modules info of a directory
    """
    def __init__(self, directory):
        self.__getInfo(directory)

    def __getInfo(self, directory):
        """
        Search all the modules for a given directoy and gets information about they.
        This meethod creates a dictionary that contains the technical name of a module
        as a key and more information as a value:
            - tecName:      Techincal name
            - name:         Name
            - path:         Path of the module
            - dependences:  Depenendences of the module
            - sons:         Sons of the module (modules that have the module as dependence)
            - found:        Shows if the module is in the given directory
            - duplicated:   Shows if the module is duplicated [TODO]
        """
        isDir = lambda fpath: os.path.isdir(fpath)
        dirs = lambda x: os.listdir(x)

        if not isDir(directory):
            raise Exception('{} Is not a valid directory'.format(directory))

        # Crear diccionario resultado
        # Cada entrada será el nombre de un módulo, que contendrá como
        # valor un diccionario con su información:
        #   - tecName:         Nombre técnico del módulo
        #   - name:         Nombre del módulo
        #   - path:         Directorio donde se encuentra el módulo (si hay más de un path indica que el módulo esta duplicado)
        #   - dependences:  Lista con las dependencias del módulo
        #   - sons:         Lista con los módulos que dependen de él
        #   - found:         Indica si el directorio esta en la ruta proporcioanda
        #   - duplicated:   Indica si el módulo esta duplicado
        self.res = {}
        queueDirs = queue.Queue(0)

        [queueDirs.put('{}/{}'.format(directory,i)) for i in dirs(directory)]

        # Recorro todos las carpetas del directorio
        while not queueDirs.empty():
            fold = queueDirs.get()

            if fold.split('/')[len(fold.split('/')) - 1] == 'setup':
                continue

            if isDir(fold):
                folders = dirs(fold)

                # Si la carpeta es un módulo
                if '__manifest__.py' in folders:
                    parse = '{}/__manifest__.py'.format(fold)
                elif '__openerp__.py' in folders:
                    parse = '{}/__openerp__.py'.format(fold)
                else:
                    # Sino, se recorren las demás carpetas
                    [queueDirs.put('{}/{}'.format(fold, i)) for i in folders]
                    continue

                # Se parse el archivo
                with open(parse, 'r') as fh:
                    parsed = eval(fh.read())
                
                moduleName = parsed.get('name', '')
                dependences = parsed.get('depends', [])
                tecName = fold.split('/')
                tecName = tecName[len(tecName) - 1]

                inRes = self.res.get(tecName, False)
                # Si el módulo esta en res y found no es true
                if inRes and not inRes['found']:
                    # Actualiza dependences, found y path
                    inRes['found'] = True
                    inRes['depends'] = dependences
                    inRes['path'] = fold
                # Si el módulo esta duplicado se lanza una excepción
                elif inRes and inRes['found']:
                    raise Exception('Módulo {} duplicado en {} y en {}'.format(
                        tecName,
                        inRes['path'],
                        fold
                    ))
                # Si no existe en res se añade al diccionario resultado
                else:
                    self.res[tecName] = {
                        'tecName': tecName,
                        'name': moduleName,
                        'depends': dependences,
                        'found': True,
                        'path': fold,
                        'sons': [],
                        'duplicated': False
                    }
                
                # Se recorren las dependencias
                for i in dependences:
                    # Si no existe en el resultado se añade
                    if i not in self.res:
                        self.res[i] = {
                            'tecName': i,
                            'name': '',
                            'depends': [],
                            'found': False,
                            'path': '',
                            'sons': [tecName],
                            'duplicated': False
                        }
                    # Si existe
                    else:
                        # Actualizo sons
                        self.res[i]['sons'].append(tecName)
        
    def writeInfo(self, fh='res.txt'):
        """
        Writes the information of all modules to a file

        :params
            [fh: file to write the information, res.txt by default]
        """
        with open('res.txt', 'w') as fh:
            for i in self.res:
                i = self.res[i]
                pr = lambda x, y: '{:<13}: {:<30}'.format(str(x), str(y))
                print(pr('Tecnical Name', i['tecName']), file=fh)
                print(pr('Name', i['name']), file=fh)
                print(pr('Depends', i['depends']), file=fh)
                print(pr('Found', i['found']), file=fh)
                print(pr('Path', i['path']), file=fh)
                print(pr('Sons', i['sons']), file=fh)
                print(pr('Duplicated', i['duplicated']), file=fh)
                print(file=fh)
    
    def getJSON(self):
        return self.res

    def getNodes(self):
        pass

    def getLinks(self):
        pass

if __name__ == '__main__':
    parser = ArgumentParser(description='Get modules of info for a given folder')

    parser.add_argument('file', type=str, help="Folder to search modules info")

    args = parser.parse_args()

    ret = Retriever(args.file)
    ret.writeInfo()