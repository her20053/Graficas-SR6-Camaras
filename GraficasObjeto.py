class Obj(object):
    def __init__(self, filename):

        self.current_material = None

        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.faces = []
        self.tvertices = []

        for line in self.lines:

            if line:

                if ' ' not in line:
                    continue

                prefix, value = line.split(' ', 1)

                if value[0] == ' ':
                    value = '' + value[1:]

                if prefix == 'o':
                    self.current_material = value

                if prefix == 'usemtl':
                    self.current_material = value

                if prefix == 'v':
                    self.vertices.append(
                        list(
                            map(float, value.split(' '))
                        )
                    )

                if prefix == 'vt':
                    self.tvertices.append(
                        list(
                            map(float, value.split(' '))
                        )
                    )

                if prefix == 'f':
                    act_face = [
                        list(map(int, face.split('/')))
                        for face in value.split(' ') if face != ''
                    ]
                    self.faces.append({
                        'material': self.current_material,
                        'face': act_face
                    })
