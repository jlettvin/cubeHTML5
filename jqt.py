#!/usr/bin/env python

HEAD = """
<html>
	<head>
                <title>Three.js: line segments</title>
		<style>canvas { width: 100%; height: 100% }</style>
	</head>
	<body>
        <h1 align="center">You need a WebGL-enabled browser to see this.</h1>
        <p align="center">
        The general shape is a paraboloid shell.
        The tips of the tubulin strands are positioned at
        precise points in a rectangular mesh.
        </p><p>
        The red arrows at the tips are z-oriented dendritic transient vector sensors (TVS).
        The green arrows at the tips are r-oriented TVS.
        The sensors feed tubulin strands which traverse from dendritic tips
        to the concentration of strands at the base.
        </p><p>

        </p>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js">
    </script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/three.js/r68/three.min.js">
    </script>
		<script>
			var scene = new THREE.Scene();
			var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);

			var renderer = new THREE.WebGLRenderer();
			renderer.setSize(window.innerWidth, window.innerHeight);
			document.body.appendChild(renderer.domElement);

			camera.position.z = 1;
			camera.position.y = 1;
			camera.position.x = 1;

                        var rotSpeed = 1e-3;

                        function checkRotation(){
                            var x = camera.position.x,
                                y = camera.position.y,
                                z = camera.position.z;


                            //if (keyboard.pressed("left"))
                            { 
                                camera.position.x = x * Math.cos(rotSpeed) + z * Math.sin(rotSpeed);
                                camera.position.z = z * Math.cos(rotSpeed) - x * Math.sin(rotSpeed);
                            //} else if (keyboard.pressed("right")){
                            /*
                                camera.position.x = x * Math.cos(rotSpeed) - z * Math.sin(rotSpeed);
                                camera.position.z = z * Math.cos(rotSpeed) + x * Math.sin(rotSpeed);
                            */
                            }
    
                            camera.lookAt(scene.position);
    
                        } 

"""

TAIL = """
			var render = function () {
				requestAnimationFrame(render);

				checkRotation();

				renderer.render(scene, camera);
			};

			render();
		</script>
	</body>
</html>
"""

BODY = """
      var material = new THREE.LineBasicMaterial(
          {color: 0x0000ff, linewidth: 3});
      var geometry = new THREE.Geometry();
      geometry.vertices.push(
	      new THREE.Vector3( -2, -2, -2 ),
	      new THREE.Vector3( +2, +2, +2 )
      );
      var line = new THREE.Line( geometry, material );
      scene.add( line );
"""

#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Common'))
#sys.path.append('..')

from cPickle import (load)
from random import (seed, randint)
from math import (sqrt)

import Tag

class Tree(object):

    def __init__(self, **kw):
        tubulin = kw.get('tubulin', None)
        pickle = kw.get('pickle', None)
        if pickle:
            #self.line = []
            self.line = load(open(pickle))
            #for strand in tubulin:
                #self.line += [[],]
                #for segment in strand:
                    #print segment
                ##print strand
                ##print '-'*70
                #pass
        elif tubulin:
            self.line = [[[-1,-1,-1], [+1,+1,+1], [-3,0,0]],]
            with open(tubulin) as source:
                for line in source:
                    element = line.split(' ')
                    assert element[0] == 'tubulin', element[0]
                    number = int(element[1][:-1])
                    triples = element[2:] #.reverse()
                    if not triples:
                        continue
                    self.line += [[],]
                    for triple in triples:
                        triple = triple.strip()
                        if not triple:
                            continue
                        triple = [float(f) for f in triple[1:-1].split(',')]
                        self.line[-1] += [triple,]
        self.Rmat = 'var Rmat = new THREE.LineBasicMaterial('
        self.Rmat += '{color: 0xff0000, linewidth: 3}'
        self.Rmat += ');\n'
        self.Gmat = 'var Gmat = new THREE.LineBasicMaterial('
        self.Gmat += '{color: 0x00ff00, linewidth: 3}'
        self.Gmat += ');\n'

    def __call__(self, **kw):
        pass

    def transientVectorSensors(self, L, geo, seg, point, scale=2e-2):
        text = ''
        x, y, z = point
        N = sqrt(x**2+y**2)
        Rgeo = 'var R%s = new THREE.Geometry();\n' % (geo)
        Ggeo = 'var G%s = new THREE.Geometry();\n' % (geo)
        Rseg = 'seg_R%d' % (L)
        Gseg = 'seg_G%d' % (L)
        text += Rgeo+Ggeo

        text += 'R%s.vertices.push(' % (geo)
        text += 'new THREE.Vector3(%f,%f,%f)' % (x,y,z)
        text += ',new THREE.Vector3(%f,%f,%f)' % (x,y,z+scale)
        text += ');\n'

        XN, YN = scale*x/N, scale*y/N
        text += 'G%s.vertices.push(' % (geo)
        text += 'new THREE.Vector3(%f,%f,%f)' % (x,y,z)
        text += ',new THREE.Vector3(%f,%f,%f)' % (x+XN,y+YN,z)
        text += ');\n'

        text += 'var R%s = new THREE.Line(R%s,Rmat);\n' % (seg, geo)
        text += 'scene.add(R%s);\n' % (seg)

        text += 'var G%s = new THREE.Line(G%s,Gmat);\n' % (seg, geo)
        text += 'scene.add(G%s);\n' % (seg)

        return text

    def rule(self, **kw):
        N = kw.get('N', 77)
        text = '//'
        text += '-'*N
        text += '\n'
        return text

    def tubulin(self, L, line):
        text = ''
        mat = 'mat_%d' % (L)
        geo = 'geo_%d' % (L)
        seg = 'seg_%d' % (L)

        text += 'var %s = new THREE.LineBasicMaterial(' % (mat)
        value = randint(0, 0xffffff)
        text += '  {color: 0x%06x, linewidth: 3}' % (value)
        text += ');\n'

        text += 'var %s = new THREE.Geometry();\n' % (geo)

        text += '%s.vertices.push(' % (geo)
        comma = ''
        for S, segment in enumerate(line):
            X, Y, Z = segment
            text += '%snew THREE.Vector3(%f,%f,%f)' % (comma,X,Y,Z)
            comma = ','
        text += ');\n'
        text += 'var %s = new THREE.Line(%s,%s);\n' % (seg, geo, mat)
        text += 'scene.add(%s);\n' % (seg)
        text += '\n'
        return text, geo, seg

    def __str__(self):
        self.body = ''
        self.body += HEAD
        self.body += self.Rmat+self.Gmat;
        for L, line in enumerate(self.line):
            text, geo, seg = self.tubulin(L, line)
            self.body += text
            self.body += self.transientVectorSensors(L, geo, seg, line[0])
            self.rule(N=77)
        self.body += TAIL
        return self.body

seed()
tree = Tree(tubulin='tubulin.20140330221624', pickle='simple.20140330221624.p')
with open('bipolar.html', 'w') as target:
    print>>target, tree
