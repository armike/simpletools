
import studioenv
import studio.maya
maya = studio.maya.importMaya()
import maya.cmds

import sys, os, traceback, time
from studio import io

from part_class_sets import PartClassSets
from part_operator import PartOperator

class Tester(PartOperator):
    """This ought to be integrated with the unittests framework.
    """

    def __init__(self, partClassObject, partClassObjectDest=None):
        super(Tester, self).__init__(partClassObject)
        
        if not partClassObjectDest:
            partClassObjectDest = PartClassSets()

        self.pcoDest = partClassObjectDest

    def run(self):
        """Run all methods ending in the name Test
        """
        methodNames = [x for x in dir(self) if x.endswith("Test")]

        results = {}
        bar = "="*70
        bar2 = "-"*70
        io.write("\n%s\n%s\n  Running Tests\n%s\n%s" % (
                bar, bar2, bar2, bar))

        for methodName in methodNames:

            self.buildUp()

            # <3 python
            # 
            cls = self.__class__
            methodObject = cls.__dict__[methodName].__get__(self, cls)
            
            stime = time.time()

            try:
                methodObject()
            except:
                excInfo = sys.exc_info()
                etime = time.time() - stime
                result = Result(
                    methodName, False, etime, exceptionInfo=excInfo)
                results[methodName] = result
            try:
                self.tearDown()
            except:
                if methodName not in results:

                    excInfo = sys.exc_info()
                    etime = time.time() - stime
                    result = Result(
                        methodName, False, etime, exceptionInfo=excInfo)
                    results[methodName] = result
                    
            if methodName not in results:
                etime = time.time() - stime
                result = Result(methodName, True, etime, None)
                results[methodName] = result

            result.printLong()

        resultList = [results[m] for m in methodNames]
        
        successCount = len([r for r in resultList if r.passed])
        
        if successCount != len(resultList):
            io.write("\n%s\n  Summary\n%s\n" % (bar2, bar2))
            [r.printShort() for r in resultList]

        io.write("\n%d/%-d tests passed." % (successCount, len(resultList)))
                
    def tearDown(self):
        """Final cleanup operations to perform
        """

    def buildUp(self):
        """Create a standard start scene for test cases.
        """
        
        maya.cmds.file(new=1, force=1)
        
        self.pco.initialize()

        self.plane = maya.cmds.polyPlane(
            n="plane",
            sx=100,
            sy=100,
            w=100,
            h=100,
            ch=0,
            )[0]
        
        self.partAFaces = "plane.f[0:900]"
        self.partBFaces = ["plane.f[1000:3900]"]
        self.partCFaces = ["plane.f[8800]", "plane.f[9000:9900]"]
        self.noPartFaces = ["plane.f[5000]", "plane.f[4000]"]
        self.partedFaces = [self.partAFaces] + self.partBFaces + self.partCFaces
        
        tempSet = self.pco.createSet("Tester_buildUp_tempSet", self.partedFaces)
        maya.cmds.sets(self.partedFaces, remove=tempSet)
        self.partlessFaces = maya.cmds.sets(tempSet, q=1)
        maya.cmds.delete(tempSet)

        self.partAName = "partA"
        self.partBName = "partB"
        self.partCName = "partC"
        self.partNoneName = "partNone"
        
        self.partAId = self.pco.getPartId(self.partAName, self.plane)
        self.partBId = self.pco.getPartId(self.partBName, self.plane)
        self.partCId = self.pco.getPartId(self.partCName, self.plane)
        self.partNoneId = self.pco.getPartId(self.partNoneName, self.plane)

        self.pco.addFacesToPart(self.partAFaces, self.partAName)
        self.pco.addFacesToPart(self.partBFaces + self.partCFaces,
                                self.partBName)
        self.pco.addFacesToPart(self.partCFaces, self.partCName)

    ######################################################################
    # Basic Method Tests
    # ------------------
    ######################################################################

    def partToFacesTest(self):
        """Test pco method: partsToFaces
        buildUp actually uses this, so we try to verify.
        """
        partAFaces = self.pco.partsToFaces(self.partAId)        
        partBFaces = self.pco.partsToFaces(self.partBId)        
        partCFaces = self.pco.partsToFaces(self.partCId)        

        assert self.contentsMatch(partAFaces, self.partAFaces)
        assert self.contentsMatch(partBFaces, self.partBFaces)
        assert self.contentsMatch(partCFaces, self.partCFaces)

    def partToFacesNoneTest(self):
        """Ensure querying an empty or nonextistant part is fine.
        """
        partNoneFaces = self.pco.partsToFaces(self.partNoneId)

        assert self.contentsMatch(partNoneFaces, [])

    def facesToPartsTest(self):
        """Test pco method: facesToParts
        """
        partAId = self.pco.facesToParts(self.partAFaces)
        partBId = self.pco.facesToParts(self.partBFaces)
        partCId = self.pco.facesToParts(self.partCFaces)
        
        assert partAId == [self.partAId]
        assert partBId == [self.partBId]
        assert partCId == [self.partCId]
        
    def facesToPartsNoneTest(self):
        """
        """
        noPartIds = self.pco.facesToParts(self.noPartFaces)
        assert(noPartIds == [])

    def deletePartsTest(self):
        self.pco.deleteParts([self.partAId, self.partBId])

        partAFaces = self.pco.partsToFaces(self.partAId)        
        partBFaces = self.pco.partsToFaces(self.partBId)        
        partCFaces = self.pco.partsToFaces(self.partCId)        
        partAId = self.pco.facesToParts(self.partAFaces)
        partBId = self.pco.facesToParts(self.partBFaces)
        partCId = self.pco.facesToParts(self.partCFaces)

        assert partAFaces == []
        assert partBFaces == []
        assert self.contentsMatch(partCFaces, self.partCFaces)
        assert partAId == []
        assert partBId == []
        assert len(partCId) == 1
        assert self.partIdsMatch(partCId[0], self.partCId)

    def partsToPartFaceDictTest(self):
        pfd = self.pco.partsToPartFaceDict(
            [self.partAId, self.partBId, self.partCId, self.partNoneId])
        
        assert self.partAId in pfd
        assert self.partBId in pfd
        assert self.partCId in pfd

        # need to make a decision about this behavior
        # 
        assert self.partNoneId in pfd

        assert self.contentsMatch(pfd[self.partAId], self.partAFaces)
        assert self.contentsMatch(pfd[self.partBId], self.partBFaces)
        assert self.contentsMatch(pfd[self.partCId], self.partCFaces)

    def objectsToPartFaceDictTest(self):
        pfd = self.pco.objectsToPartFaceDict(self.plane)

        pairs = pfd.items()
        pairs.sort(key=lambda x: x[0])

        partAId,partAFaces = pairs[0]
        partBId,partBFaces = pairs[1]
        partCId,partCFaces = pairs[2]

        assert len(pfd) == 3
        assert self.partIdsMatch(self.partAId, partAId)
        assert self.partIdsMatch(self.partBId, partBId)
        assert self.partIdsMatch(self.partCId, partCId)

        assert self.contentsMatch(self.partAFaces, self.partAFaces)
        assert self.contentsMatch(self.partBFaces, self.partBFaces)
        assert self.contentsMatch(self.partCFaces, self.partCFaces)


    def renamePartsTest(self):
        expectedNewPartNameA = "newPartNameA"
        expectedNewPartNameB = "newPartNameB"
        newNames = [expectedNewPartNameA, expectedNewPartNameB]

        partIdsToRename = [self.partAId, self.partBId]
        newPartIds = self.pco.renameParts(partIdsToRename, newNames)
        
        facesA = self.pco.partsToFaces(newPartIds[0])
        facesB = self.pco.partsToFaces(newPartIds[1])
        facesC = self.pco.partsToFaces(self.partCId)

        partNameA = self.pco.getPartName(newPartIds[0])
        partNameB = self.pco.getPartName(newPartIds[1])

        assert partNameA == expectedNewPartNameA
        assert partNameB == expectedNewPartNameB

        assert self.contentsMatch(facesA, self.partAFaces)
        assert self.contentsMatch(facesB, self.partBFaces)
        assert self.contentsMatch(facesC, self.partCFaces)
    
    ######################################################################
    # Workflow Tests
    # ---------------
    ######################################################################

    def assignEditSaveOpenDuplicateTest(self):
        
        vtx = "%s.vtx[0]" % (self.plane)

        maya.cmds.xform(vtx, r=1, translation=(0, 1, 0))

        self.exportTempFile()
        self.openFile()
        self.deleteTempFile()

        dup = maya.cmds.duplicate(self.plane, rr=1, upstreamNodes=0)[0]
        
        self.assertMeshPartsMatch(self.plane, dup)

    def assignEditSaveOpenDuplicateWithHistoryTest(self):
        
        vtx = "%s.vtx[0]" % (self.plane)

        maya.cmds.xform(vtx, r=1, translation=(0, 1, 0))

        self.exportTempFile()
        self.openFile()
        self.deleteTempFile()

        dup = maya.cmds.duplicate(self.plane, rr=1, upstreamNodes=1)[0]
        
        self.assertMeshPartsMatch(self.plane, dup)


    def polySplitTest(self):
        
        maya.cmds.polySplit(self.plane, ch=0, s=1, sma=0,
                            ip=([201, 0.535178], [0, 0.5]))

        maya.cmds.polySplit(self.plane, ch=0, s=1, sma=0,
                            ip=([20202, 0.552689], [5, 0.5]))

        maya.cmds.polySplit(self.plane, ch=0, s=1, sma=0,
                            ip=([1, 0.542349], [3, 0.577837]))
                            
        expectedNewPartAFaces = [u'plane.f[0:900]', u'plane.f[10000:10004]']
        expectedNewPartBFaces = [u'plane.f[1000:3900]']
        expectedNewPartCFaces = [u'plane.f[8800]', u'plane.f[9000:9900]']
        
        partAFaces = self.pco.partsToFaces(self.partAId)
        partBFaces = self.pco.partsToFaces(self.partBId)
        partCFaces = self.pco.partsToFaces(self.partCId)

        assert self.contentsMatch(expectedNewPartAFaces, partAFaces)
        assert self.contentsMatch(expectedNewPartBFaces, partBFaces)
        assert self.contentsMatch(expectedNewPartCFaces, partCFaces)

    def polySplitWithHistoryTest(self):
        
        maya.cmds.polySplit(self.plane, ch=1, s=1, sma=0,
                            ip=([201, 0.535178], [0, 0.5]))

        maya.cmds.polySplit(self.plane, ch=1, s=1, sma=0,
                            ip=([20202, 0.552689], [5, 0.5]))

        maya.cmds.polySplit(self.plane, ch=1, s=1, sma=0,
                            ip=([1, 0.542349], [3, 0.577837]))
                            
        expectedNewPartAFaces = [u'plane.f[0:900]', u'plane.f[10000:10004]']
        expectedNewPartBFaces = [u'plane.f[1000:3900]']
        expectedNewPartCFaces = [u'plane.f[8800]', u'plane.f[9000:9900]']
        
        partAFaces = self.pco.partsToFaces(self.partAId)
        partBFaces = self.pco.partsToFaces(self.partBId)
        partCFaces = self.pco.partsToFaces(self.partCId)

        assert self.contentsMatch(expectedNewPartAFaces, partAFaces)
        assert self.contentsMatch(expectedNewPartBFaces, partBFaces)
        assert self.contentsMatch(expectedNewPartCFaces, partCFaces)

    ######################################################################
    # Testing Utils
    # ---------------
    ######################################################################

    def assertMeshPartsMatch(self, a, b):
        """Given two separate mesh parts, ensure the partNames and corresponding
        faces match.
        """
        aParts = self.pco.objectsToParts(a)
        bParts = self.pco.objectsToParts(b)
        
        aParts.sort()
        bParts.sort()

        aNames = self.pco.getPartNames(aParts)
        bNames = self.pco.getPartNames(bParts)

        assert aNames == bNames
        
        for aPart, bPart in zip(aParts, bParts):
            aFaces = self.pco.partsToFaces(aPart)
            bFaces = self.pco.partsToFaces(bPart)
            aIndices = [f.split(".")[-1] for f in aFaces]
            bIndices = [f.split(".")[-1] for f in bFaces]
            assert aIndices == bIndices
        

    def contentsMatch(self, a, b):
        """Return True if A's contents equals B's.  Meant to be used for
        comparing lists of maya objects, which can differ in representation.
        """
        try:

            aContents = maya.cmds.ls(a, l=1, fl=1)
            bContents = maya.cmds.ls(b, l=1, fl=1)

        except:

            return False

        return aContents == bContents
        
    def partIdsMatch(self, a, b):
        """Determine if partIds match.
        """
        return self.pco.canonizePartId(a) == self.pco.canonizePartId(b)
                       
    def exportTempFile(self, filepath=None):
        """
        """
        if not filepath:
            filepath = self.getTempFilePath()

        maya.cmds.file(filepath, force=1, exportAll=1, type="mayaAscii")

    def openFile(self, filepath=None):
        """
        """
        if not filepath:
            filepath = self.getTempFilePath()

        maya.cmds.file(filepath, force=1, open=1, options="v=0", type="mayaAscii")        

    def deleteTempFile(self, filepath=None):
        if not filepath:
            filepath = self.getTempFilePath()
        
        os.remove(filepath)

    def getTempFilePath(self):
        """
        """
        return "g:/parts_test_temp.ma"
    
class Result():
    """Test Result object.
    """
    def __init__(self, testName, passed, runtime, exceptionInfo=None):
        """
        """
        self.testName = testName
        self.passed = passed
        self.runtime = runtime
        self.exceptionInfo = exceptionInfo

    def printShort(self):
        """
        """
        status = "Pass!" if self.passed else "-- FAIL --"
        prefix = "%s:" % self.testName
        io.write("%-40s  %-12s time: %.3f" % (prefix, status, self.runtime))

    def printLong(self):
        """
        """
        if not self.passed:
            bar = "-"*70
            io.write("\n%s\n%s  %.3f\n%s" % (
                    bar, self.testName, self.runtime, bar))
            ei = self.exceptionInfo
            traceback.print_exception(ei[0], ei[1], ei[2])
            
        else:
            self.printShort()
