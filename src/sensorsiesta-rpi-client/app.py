import rpyc


conn = rpyc.connect("localhost", 8000)
dao = conn.root

dao.createByValues(intMember = 74)
dao.updateByValues(1, strMember = 'updated str member')
dao.deleteById(3)

