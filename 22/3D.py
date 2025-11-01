from direct.showbase.Showbase import ShowBase
from direct.actor.Actor import Actor

class MyApp(ShowBase):
    def_init_(self):
        super()._init_()

        self.model = self.loader.loadModel("models/panda-model")
        self.character = Actor("character.glb", {"walk" : "C:\Users\HP\Downloads\Walking.fbx"})
        self.model.reparentTo(self.render)
        self.model.setScale(1)
        self.model.setPos(0, 10, 0)
        self.character.loop("walk")

app = MyApp()
app.run()