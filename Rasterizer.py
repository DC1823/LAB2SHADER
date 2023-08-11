from gl import Renderer, P2, P3, color
import shaders

width=700
height=700
render=Renderer(width,height)
render.cfondo()
render.vShader=shaders.vShader
render.glMirar(cpos=(1,0,0), epos=(0,0,0))
render.fragShader=shaders.invShader
render.glLoadM("./modelo/perro.obj", "./textura/perro.bmp",trans=(0,0,0), rotar=(0,0,0), escala=(0.01,0.01,0.01))
render.glRender()

render.glFinish("output3.bmp")