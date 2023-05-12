from qgis.gui import QgsLayerTreeView
from qgis.gui import QgisInterface
from qgis.core import QgsLayerTree
from qgis.core import QgsLayerTreeNode
from qgis.core import QgsProject
from qgis.gui import *
import processing

하천명 = "신탄진" #해당 그룹명을 써야함
해당레이어 = ("B0010000")#"F0010000" "A0010000" "B0010000" "A0020000" ("E0010001", "E0052114")

root = QgsProject.instance().layerTreeRoot()
iface.layerTreeView().setCurrentLayer(None) #빠르게 전체선택해제
for child in root.children():
    #print ("- group: " + child.name())
    if child.name() == 하천명: #to check subgroups within test group
        for subChild in child.children():
            subChild.name()
            if subChild.name() == "기초지도":
                
                for lastChild in subChild.children():
                    lastChild.name()
                    for EndChild in lastChild.children():
                        if isinstance(lastChild, QgsLayerTreeGroup):
                            EndChild.name()
                            #print(EndChild.name())
                            if EndChild.name() in 해당레이어:
                            #if EndChild.name() == 해당레이어:
                                
                                iface.layerTreeView().setSelectionMode( QAbstractItemView.MultiSelection )
                                iface.setActiveLayer(EndChild.layer())
                                #List.add.iface.activeLayer()
                                #List = iface.activeLayer()
                                #print(List)
                                #processing.runAndLoadResults("native:mergevectorlayers",{'LAYERS':[List],'CRS':QgsCoordinateReferenceSystem('EPSG:5186'),'OUTPUT':'TEMPORARY_OUTPUT'})
                                #iface.layerTreeView().setSelectionMode( QAbstractItemView.ExtendedSelection )
                                
#iface.layerTreeView().selectedLayers()
#iface.layerTreeView()
#List = iface.activeLayer()
List = iface.layerTreeView().selectedLayers()
print(List)
#iface.layerTreeView().activeLayer()
processing.runAndLoadResults("native:mergevectorlayers",
{'LAYERS':List,'CRS':QgsCoordinateReferenceSystem('EPSG:5186'),
'OUTPUT':'TEMPORARY_OUTPUT'})

#processing.runAndLoadResults("native:mergevectorlayers",{'LAYERS':List,'CRS':QgsCoordinateReferenceSystem('EPSG:5186'),'OUTPUT':'TEMPORARY_OUTPUT'})
iface.layerTreeView().setSelectionMode( QAbstractItemView.ExtendedSelection )
#iface.layerTreeView().setCurrentLayer(None)


