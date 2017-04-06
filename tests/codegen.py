import os
import shutil
import subprocess
import tempfile
import unittest

from cozy.target_syntax import *
from cozy.syntax_tools import pprint
from cozy.compile import CxxPrinter
from cozy.library import Library
from cozy.autotuning import enumerate_impls
from cozy.sharing import compute_sharing

class TestCodegen(unittest.TestCase):

    def test_regression1(self):
        PixMap = TNative("int")
        ByteArray = TNative("int")
        Enum = TEnum(('Disk', 'Loading', 'DiskAndMemory', 'MemoryOnly', 'Saving', 'NetworkPending', 'IndexPending', 'Invalid'))
        Entry = THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool()))))
        spec = Spec('TileCache', [('State', Enum), ('Key', TNative('uint64_t')), ('Entry', Entry)], [], [('_var406', TMap(TNative('uint64_t'), TBag(Entry)))], [], [Query('_name28', [('e', Entry)], (), EEmptyList().with_type(TBag(TNative('uint64_t')))), Query('_name261', [('e', Entry), ('_var251', TNative('uint64_t'))], (), EEmptyList().with_type(TBag(Entry))), Query('_name260', [('e', Entry)], (), ESingleton(EGetField(EGetField(EVar('e').with_type(Entry), 'val').with_type(TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))), 'key').with_type(TNative('uint64_t'))).with_type(TBag(TNative('uint64_t')))), Query('_name25', [('e', Entry)], (), EEmptyList().with_type(TBag(TNative('uint64_t')))), Query('_name33', [('e', Entry), ('_var19', TNative('uint64_t'))], (), ESingleton(EVar('e').with_type(Entry)).with_type(TBag(Entry))), Query('_name257', [('e', Entry)], (), EEmptyList().with_type(TBag(TNative('uint64_t')))), Query('_name266', [('e', Entry), ('_var251', TNative('uint64_t'))], (), EEmptyList().with_type(TBag(Entry))), Query('_name22', [('e', Entry)], (), ESingleton(EGetField(EGetField(EVar('e').with_type(Entry), 'val').with_type(TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))), 'key').with_type(TNative('uint64_t'))).with_type(TBag(TNative('uint64_t')))), Query('_name37', [('_var19', TNative('uint64_t')), ('e', Entry)], (), EEmptyList().with_type(TBag(Entry))), Query('_name29', [('e', Entry), ('_var19', TNative('uint64_t'))], (), ESingleton(EVar('e').with_type(Entry)).with_type(TBag(Entry))), Query('findTile', [('k', TNative('uint64_t'))], (), EUnaryOp('the', EMapGet(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('k').with_type(TNative('uint64_t'))).with_type(TBag(Entry))).with_type(TMaybe(Entry))), Query('_name270', [('_var251', TNative('uint64_t')), ('e', Entry)], (), EMapGet(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var251').with_type(TNative('uint64_t'))).with_type(TBag(Entry))), Op('add', [('e', Entry)], [], SSeq(SSeq(SForEach(EVar('_var19').with_type(TNative('uint64_t')), ECall('_name28', [EVar('e').with_type(Entry)]).with_type(TBag(TNative('uint64_t'))), SMapDel(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var19').with_type(TNative('uint64_t')))), SForEach(EVar('_var19').with_type(TNative('uint64_t')), ECall('_name22', [EVar('e').with_type(Entry)]).with_type(TBag(TNative('uint64_t'))), SMapPut(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var19').with_type(TNative('uint64_t')), ECall('_name29', [EVar('e').with_type(Entry), EVar('_var19').with_type(TNative('uint64_t'))]).with_type(TBag(Entry))))), SForEach(EVar('_var19').with_type(TNative('uint64_t')), ECall('_name25', [EVar('e').with_type(Entry)]).with_type(TBag(TNative('uint64_t'))), SMapUpdate(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var19').with_type(TNative('uint64_t')), EVar('_var38').with_type(TBag(Entry)), SSeq(SForEach(EVar('_var39').with_type(Entry), ECall('_name33', [EVar('e').with_type(Entry), EVar('_var19').with_type(TNative('uint64_t'))]).with_type(TBag(Entry)), SCall(EVar('_var38').with_type(TBag(Entry)), 'add', [EVar('_var39').with_type(Entry)])), SForEach(EVar('_var40').with_type(Entry), ECall('_name37', [EVar('_var19').with_type(TNative('uint64_t')), EVar('e').with_type(Entry)]).with_type(TBag(Entry)), SCall(EVar('_var38').with_type(TBag(Entry)), 'remove', [EVar('_var40').with_type(Entry)]))))))), Op('rm', [('e', Entry)], [], SSeq(SSeq(SForEach(EVar('_var251').with_type(TNative('uint64_t')), ECall('_name260', (EVar('e').with_type(Entry),)).with_type(TBag(TNative('uint64_t'))), SMapDel(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var251').with_type(TNative('uint64_t')))), SForEach(EVar('_var251').with_type(TNative('uint64_t')), ECall('_name28', (EVar('e').with_type(Entry),)).with_type(TBag(TNative('uint64_t'))), SMapPut(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var251').with_type(TNative('uint64_t')), ECall('_name261', (EVar('e').with_type(Entry), EVar('_var251').with_type(TNative('uint64_t')))).with_type(TBag(Entry))))), SForEach(EVar('_var251').with_type(TNative('uint64_t')), ECall('_name257', (EVar('e').with_type(Entry),)).with_type(TBag(TNative('uint64_t'))), SMapUpdate(EVar('_var406').with_type(TMap(TNative('uint64_t'), TBag(Entry))), EVar('_var251').with_type(TNative('uint64_t')), EVar('_var271').with_type(TBag(Entry)), SSeq(SForEach(EVar('_var272').with_type(Entry), ECall('_name266', (EVar('e').with_type(Entry), EVar('_var251').with_type(TNative('uint64_t')))).with_type(TBag(Entry)), SCall(EVar('_var271').with_type(TBag(Entry)), 'add', [EVar('_var272').with_type(Entry)])), SForEach(EVar('_var273').with_type(Entry), ECall('_name270', (EVar('_var251').with_type(TNative('uint64_t')), EVar('e').with_type(Entry))).with_type(TBag(Entry)), SCall(EVar('_var271').with_type(TBag(Entry)), 'remove', [EVar('_var273').with_type(Entry)])))))))])
        state_map = {'_var406': EMakeMap(EVar('entries').with_type(TBag(THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))))), ELambda(EVar('_var19').with_type(THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool()))))), EGetField(EGetField(EVar('_var19').with_type(THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool()))))), 'val').with_type(TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))), 'key').with_type(TNative('uint64_t'))), ELambda(EVar('_var20').with_type(TBag(THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))))), EVar('_var20').with_type(TBag(THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))))))).with_type(TMap(TNative('uint64_t'), TBag(THandle('Entry', TRecord((('key', TNative('uint64_t')), ('pixmap', PixMap), ('indexData', ByteArray), ('memSize', TInt()), ('diskSize', TInt()), ('st', Enum), ('inUse', TBool())))))))}
        print(pprint(spec))
        lib = Library()
        impls = list(enumerate_impls(spec, lib))
        print("# impls: {}".format(len(impls)))
        dir = tempfile.mkdtemp()
        print("Writing impls to {}".format(dir))
        codgen = CxxPrinter()
        for i in range(len(impls)):
            impl = impls[i]
            filename = os.path.join(dir, "impl_{}.cxx".format(i))
            args = ["c++", "-std=c++11", "-c", filename, "-o", "/dev/null"]
            print("[impl {}] Running {}".format(i, " ".join(args)))

            share_info = compute_sharing(state_map, dict(impl.statevars))
            print(share_info)
            with open(filename, "w") as f:
                f.write(codgen.visit(impl, state_map, share_info))
            res = subprocess.run(["c++", "-std=c++11", "-c", filename, "-o", "/dev/null"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(res.stdout.decode("UTF-8"))
            print(res.stderr.decode("UTF-8"))
            assert res.returncode == 0
        shutil.rmtree(dir)
