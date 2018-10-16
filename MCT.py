class Node:
    def __init__(self, value, id=0):
        (gameState, t, n) = value
        self.id = id
        self.children = []
        self.value = (gameState, float(t), float(n))
        self.isLeaf = True

    def addChild(self, child):
        self.children.append(child)

    def chooseChild(self):
        _, _, pn = self.value
        maxUCB = -999999
        bestChild = None
        for i in self.children:
            _, t, n = i.value
            if n == 0:
                return i
            UCB = t + 1.96 * math.sqrt(math.log(pn) / n)
            if maxUCB < UCB:
                maxUCB = UCB
                bestChild = i
        return bestChild

    def findParent(self, node):
        for i in self.children:
            if i == node:
                return self
            else:
                possibleParent = i.findParent(node)
                if possibleParent != None:
                    return possibleParent

    def __str__(self):
        (_, t, n) = self.value
        id = self.id
        return "Node " + str(id) + ", t = " + str(t) + ", n = " + str(n)


class Tree:
    def __init__(self, root):
        self.count = 1
        self.tree = root
        self.leaf = [root.value[0]]

    def insert(self, parent, child):
        id = self.count
        self.count += 1
        child.id = id
        parent.addChild(child)
        if parent.value[0] in self.leaf:
            self.leaf.remove(parent.value[0])
        parent.isLeaf = False
        self.leaf.append(child.value[0])

    def getParent(self, node):
        if node == self.tree:
            return None
        return self.tree.findParent(node)

    def backPropagate(self, r, node):
        (gameState, t, n) = node.value
        node.value = (gameState, t + r, n + 1)
        parent = self.getParent(node)
        if parent != None:
            self.backPropagate(r, parent)

    def select(self, node=None):
        if node == None:
            node = self.tree
        if not node.isLeaf:
            nextNode = node.chooseChild()
            return self.select(nextNode)
        else:
            return node

  def iteration(self, mct):
      if mct.tree.children == []:
          self.expand(mct, mct.tree)
      else:
          leaf = mct.select()
          if leaf.value[2] == 0:
              r = self.OfsRollout(leaf.value[0])
              mct.backPropagate(r, leaf)
          elif leaf.value[2] == 1:
              self.expand(mct, leaf)
              newLeaf = random.choice(leaf.children)
              r = self.OfsRollout(newLeaf.value[0])
              mct.backPropagate(r, newLeaf)

  def expand(self, mct, node):
      actions = node.value[0].getLegalActions(self.index)
      actions.remove(Directions.STOP)
      for action in actions:
          successor = node.value[0].generateSuccessor(self.index, action)
          successorNode = Node((successor, 0, 0))
          mct.insert(node, successorNode)
