import bedrock
import numpy as np
import json
from tkinter import DoubleVar,StringVar,IntVar, Label, Entry, Tk, Button, Listbox, Toplevel,Checkbutton,BooleanVar,END, ANCHOR
filename="test"
from tkinter import filedialog
from queue import Queue
from zipfile import ZipFile
import os
import shutil
overworld=0
nether=1
theEnd=2




worldExtense=[[-10000,10000],[-10000,10000]]

def checkChunk(world,x,z,dim):
    try:
        bedrock.Chunk(world.db,x,z,dim)
        chunk=True
    except:
        chunk=False
    return chunk
def checkBlock(world,x,z):
    try:
        world.getBlock(x,z,2)
        chunk=True
    except:
        chunk=False
    return chunk
def deleteChunk(world,x,z,dim):
    if(checkChunk(world,x,z,dim)):
        chunk=bedrock.Chunk(world.db,x,z,dim)
        chunk.delete(world.db)






class deleteZoneWindow:
    def __init__(self,master,deleteque):
        self.deleteQue=deleteque
        self.XMax = IntVar()
        self.XMin = IntVar()
        self.ZMax = IntVar()
        self.ZMin = IntVar()
        self.overworld=BooleanVar()
        self.nether=BooleanVar()
        self.theEnd=BooleanVar()
        self.nameVar=StringVar()
        

        r=0
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Name").grid(row=r,column=1)
        Entry(master=top,textvariable=self.nameVar,width=37,borderwidth=1).grid(row=r,column=2,columnspan=4)
        r+=1
        Label(self.top, text="X Min",borderwidth=1 ).grid(row=r,column=2)
        Label(self.top, text="X Max",borderwidth=1 ).grid(row=r,column=3)
        Label(self.top, text="Z Min",borderwidth=1 ).grid(row=r,column=4)
        Label(self.top, text="Z Max",borderwidth=1 ).grid(row=r,column=5)
        r+=1
        Label(self.top, text="Overworld",borderwidth=1 ).grid(row=r,column=1)
        Entry(self.top, textvariable=self.XMax,borderwidth=1,width=5).grid(row=r,column=2)
        Entry(self.top, textvariable=self.XMin,borderwidth=1,width=5).grid(row=r,column=3)
        Entry(self.top, textvariable=self.ZMax,borderwidth=1,width=5).grid(row=r,column=4)
        Entry(self.top, textvariable=self.ZMin,borderwidth=1,width=5).grid(row=r,column=5)
        r+=1
        Checkbutton(self.top, text='Overworld',variable=self.overworld).grid(row=r,column=1)
        r+=1
        Checkbutton(self.top, text='Nether',variable=self.nether).grid(row=r,column=1)
        r+=1
        Checkbutton(self.top, text='End',variable=self.theEnd).grid(row=r,column=1)
        r+=1
        Button(top,text='Done',command=self.cleanup).grid(row=r,column=3)
    def cleanup(self):
        xvals=[self.XMax.get(),self.XMin.get()]
        zvals=[self.ZMax.get(),self.ZMin.get()]
        xmax=max(xvals)
        xmin=min(xvals)
        zmax=max(zvals)
        zmin=min(zvals)
        deleteVal={}
        if self.overworld.get():
            deleteVal[overworld]={}
            deleteVal[overworld][self.nameVar.get()]={"xstart":xmin, "xstop":xmax, "zstart":zmin, "zstop":zmax}

        if self.nether.get():
            deleteVal[nether]={}
            deleteVal[nether][self.nameVar.get()]={"xstart":xmin, "xstop":xmax, "zstart":zmin, "zstop":zmax}

        if self.theEnd.get():
            deleteVal[theEnd]={}
            deleteVal[theEnd][self.nameVar.get()]={"xstart":xmin, "xstop":xmax, "zstart":zmin, "zstop":zmax}
        self.deleteQue.put(deleteVal)
        ##self.value=self.e.get()
        self.top.destroy()


class mainWindow:
    def __init__(self,master):
        self.delete=delete={overworld:{},nether:{},theEnd:{}}
        
        self.master=master
        self.master.title("Mad Hatter's World Pruner")
        self.worldFile = StringVar()
        self.OWXMax = IntVar()
        self.OWXMin = IntVar()
        self.OWZMax = IntVar()
        self.OWZMin = IntVar()
        self.OWXMax.set(20000)
        self.OWXMin.set(-20000)
        self.OWZMax.set(20000)
        self.OWZMin.set(-20000)
        
        self.NeXMax = IntVar()
        self.NeXMin = IntVar()
        self.NeZMax = IntVar()
        self.NeZMin = IntVar()
        
        self.NeXMax.set(20000)
        self.NeXMin.set(-20000)
        self.NeZMax.set(20000)
        self.NeZMin.set(-20000)
        
        self.EndXMax = IntVar()
        self.EndXMin = IntVar()
        self.EndZMax = IntVar()
        self.EndZMin = IntVar()
        
        self.save={overworld:{self.OWXMax.get()},
                   nether:{},
                   theEnd:{}}

        r=0

        Label(self.master, text="World File",borderwidth=1).grid(row=r,column=1)
        Entry(self.master, textvariable=self.worldFile,borderwidth=1, width=40).grid(row=r,column=2,columnspan=3)
        Button(self.master, text="Browse",command=self.browseWorld,borderwidth=1 ).grid(row=r,column=5)
        r+=1
        Label(self.master, text="X Min",borderwidth=1 ).grid(row=r,column=2)
        Label(self.master, text="X Max",borderwidth=1 ).grid(row=r,column=3)
        Label(self.master, text="Z Min",borderwidth=1 ).grid(row=r,column=4)
        Label(self.master, text="Z Max",borderwidth=1 ).grid(row=r,column=5)
        r+=1
        Label(self.master, text="Overworld",borderwidth=1 ).grid(row=r,column=1)
        Entry(self.master, textvariable=self.OWXMin,borderwidth=1,width=6).grid(row=r,column=2)
        Entry(self.master, textvariable=self.OWXMax,borderwidth=1,width=6).grid(row=r,column=3)
        Entry(self.master, textvariable=self.OWZMin,borderwidth=1,width=6).grid(row=r,column=4)
        Entry(self.master, textvariable=self.OWZMax,borderwidth=1,width=6).grid(row=r,column=5)
        r+=1
        Label(self.master, text="Nether",borderwidth=1 ).grid(row=r,column=1)
        Entry(self.master, textvariable=self.NeXMin,borderwidth=1,width=6).grid(row=r,column=2)
        Entry(self.master, textvariable=self.NeXMax,borderwidth=1,width=6).grid(row=r,column=3)
        Entry(self.master, textvariable=self.NeZMin,borderwidth=1,width=6).grid(row=r,column=4)
        Entry(self.master, textvariable=self.NeZMax,borderwidth=1,width=6).grid(row=r,column=5)
        
        r+=1
        Label(self.master, text="End",borderwidth=1).grid(row=r,column=1)
        Entry(self.master, textvariable=self.EndXMin,borderwidth=1,width=6).grid(row=r,column=2)
        Entry(self.master, textvariable=self.EndXMax,borderwidth=1,width=6).grid(row=r,column=3)
        Entry(self.master, textvariable=self.EndZMin,borderwidth=1,width=6).grid(row=r,column=4)
        Entry(self.master, textvariable=self.EndZMax,borderwidth=1,width=6).grid(row=r,column=5)
        
        

        r+=1
        Label(self.master, text="Delete Zones",borderwidth=1 ).grid(row=r,column=1)
        self.listbox = Listbox(self.master)
        self.listbox.grid(row=r,column=2,columnspan=3,rowspan=2)
        self.addButton=Button(self.master, text="Add Delete Zone",command=lambda: self.addDeleteZone())
        self.addButton.grid(row=r,column=5)
        r+=1
        self.delButton=Button(self.master, text="Remove Delete Zone",command=self.deleteSkin ).grid(row=r,column=5)
        r+=1
        self.delButton=Button(self.master, text="Export",command=self.pruneWorld ).grid(row=r,column=5)
    def addDeleteZone(self):
        deleteQue=Queue()
        w=deleteZoneWindow(self.listbox,deleteQue)
        self.addButton["state"]="disabled"
        root.wait_window(w.top)
        self.addButton["state"] = "normal"
        deleteJson=deleteQue.get()
        for key in deleteJson.keys():
            self.delete[key].update(deleteJson[key])
        name=list(self.delete[key].keys())[0]
        print(name)
        self.listbox.insert(END,name)
    def browseWorld(self):
        self.worldFile.set(filedialog.askopenfilename(filetypes = (("World files", "*.mcworld"),("World Files","*.zip") )))
    def deleteSkin(self):
        items = self.listbox.curselection()
        name=self.listbox.get(self.listbox.curselection())
        print(self.delete)
        if len(items)>0:
            print(name)
            for dim in self.delete.keys():
                
                if name in list(self.delete[dim].keys()):
                    self.delete[dim].pop(name)
            self.listbox.delete(ANCHOR)
        print(self.delete)
    def pruneWorld(self):
        owx=[self.OWXMax.get(),self.OWXMin.get()]
        owz=[self.OWZMax.get(),self.OWZMin.get()]
        nex=[self.NeXMax.get(),self.NeXMin.get()]
        nez=[self.NeZMax.get(),self.NeZMin.get()]
        ex=[self.EndXMax.get(),self.EndXMin.get()]
        ez=[self.EndZMax.get(),self.EndZMin.get()]
        self.save={overworld:{},
                   nether:{},
                   theEnd:{}}
        self.save[overworld]={"xstart":min(owx), "xstop":max(owx), "zstart":min(owz), "zstop":max(owz)}
        self.save[nether]={"xstart":min(nex), "xstop":max(nex), "zstart":min(nez), "zstop":max(nez)}
        self.save[theEnd]={"xstart":min(ex), "xstop":max(ex), "zstart":min(ez), "zstop":max(ez)}
        templateWorld=self.worldFile.get()
        path_to_save="temp"
        outputFileName=templateWorld.replace(".mcworld","").replace(".MCWORLD","").replace(".zip","").replace(".ZIP","")
        
        if not os.path.isdir(path_to_save):#make a temp folder to work out of
            os.mkdir(path_to_save)
        else:
            for filename in os.listdir(path_to_save):
                file_path = os.path.join(path_to_save, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        with ZipFile(templateWorld, 'r') as zipObj:
            zipObj.extractall(path_to_save)
        with bedrock.World(path_to_save) as world:
            for dim in [overworld,nether,theEnd]:
                saLim=self.save[dim]
                print(saLim)
                for blockX in np.arange(start=worldExtense[0][0],stop=worldExtense[0][1],step=16):
                    for blockZ in np.arange(start=worldExtense[1][0],stop=worldExtense[1][1],step=16):
                        chunkX=blockX//16
                        chunkZ=blockZ//16
                        
                        if  saLim["zstart"]<blockZ and  saLim["zstop"]>blockZ and  saLim["xstart"]<blockX and  saLim["xstop"]>blockX:
                            pass
                        else:
                            deleteChunk(world,chunkX,chunkZ,dim)
                        for name in self.delete[dim].keys():
                            delLim=self.delete[dim][name]
                            if delLim["zstart"]<blockZ and delLim["zstop"]>blockZ and delLim["xstart"]<blockX and delLim["xstop"]>blockX:
                                deleteChunk(world,chunkX,chunkZ,dim)
        startDir=os.getcwd()
        os.chdir(os.path.join(startDir,path_to_save))
        with ZipFile(outputFileName+"-pruned.mcworld", 'w') as zipF:
            zipF.write("world_icon.jpeg")
            zipF.write("levelname.txt")
            zipF.write("level.dat_old")
            zipF.write("level.dat")
            for root, dirs, files in os.walk("db"):
                for file in files:
                    zipF.write(os.path.join(root, file))
        ##pack up world 
        shutil.move(os.path.join(os.getcwd(),outputFileName+".mcworld"),os.path.join(startDir,outputFileName+".mcworld"))
        #print blocks required.
        print("done")

root = Tk()
m=mainWindow(root)
root.mainloop(  )
