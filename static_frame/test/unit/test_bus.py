import unittest
# from io import StringIO
import numpy as np # type: ignore

from static_frame.core.frame import Frame
from static_frame.core.bus import Bus
# from static_frame.core.bus import FrameDeferred

from static_frame.core.series import Series

from static_frame.core.store import StoreZipTSV

from static_frame.test.test_case import TestCase
from static_frame.test.test_case import temp_file
from static_frame.test.test_case import skip_win

# from static_frame.test.test_case import skip_win
from static_frame.core.exception import ErrorInitBus


class TestUnit(TestCase):

    def test_bus_init_a(self) -> None:

        f1 = Frame.from_dict(
                dict(a=(1,2), b=(3,4)),
                index=('x', 'y'),
                name='foo')
        f2 = Frame.from_dict(
                dict(a=(1,2,3), b=(4,5,6)),
                index=('x', 'y', 'z'),
                name='bar')

        b1 = Bus.from_frames((f1, f2))

        self.assertEqual(b1.keys().values.tolist(),
                ['foo', 'bar'])


        with temp_file('.zip') as fp:
            b1.to_zip_tsv(fp)
            b2 = Bus.from_zip_tsv(fp)

            f3 = b2['bar']
            f4 = b2['foo']
            # import ipdb; ipdb.set_trace()
            zs = StoreZipTSV(fp)
            zs.write(b1.items())

            f3 = zs.read('foo')
            self.assertEqual(
                f3.to_pairs(0),
                (('a', (('x', 1), ('y', 2))), ('b', (('x', 3), ('y', 4))))
            )

    def test_bus_init_b(self) -> None:

        with self.assertRaises(ErrorInitBus):
            Bus(Series([1, 2, 3]))

        with self.assertRaises(ErrorInitBus):
            Bus(Series([3, 4], dtype=object))


    def test_bus_shapes_a(self) -> None:
        f1 = Frame.from_dict(
                dict(a=(1,2), b=(3,4)),
                index=('x', 'y'),
                name='f1')
        f2 = Frame.from_dict(
                dict(a=(1,2,3), b=(4,5,6)),
                index=('x', 'y', 'z'),
                name='f2')
        f3 = Frame.from_dict(
                dict(a=(10,20), b=(50,60)),
                index=('p', 'q'),
                name='f3')

        b1 = Bus.from_frames((f1, f2, f3))

        with temp_file('.zip') as fp:

            b1.to_zip_pickle(fp)

            b2 = Bus.from_zip_pickle(fp)

            f2_loaded = b2['f2']

            self.assertEqual(b2.shapes.to_pairs(),
                    (('f1', None), ('f2', (3, 2)), ('f3', None)))

            f3_loaded = b2['f3']

            self.assertEqual(b2.shapes.to_pairs(),
                    (('f1', None), ('f2', (3, 2)), ('f3', (2, 2 )))
                    )

    @skip_win # type: ignore
    def test_bus_nbytes_a(self) -> None:
        f1 = Frame.from_dict(
                dict(a=(1,2), b=(3,4)),
                index=('x', 'y'),
                name='f1')
        f2 = Frame.from_dict(
                dict(a=(1,2,3), b=(4,5,6)),
                index=('x', 'y', 'z'),
                name='f2')
        f3 = Frame.from_dict(
                dict(a=(10,20), b=(50,60)),
                index=('p', 'q'),
                name='f3')

        b1 = Bus.from_frames((f1, f2, f3))

        with temp_file('.zip') as fp:
            b1.to_zip_pickle(fp)
            b2 = Bus.from_zip_pickle(fp)

            f2_loaded = b2['f2']

            self.assertEqual(b2.nbytes, 48)

            f3_loaded = b2['f3']

            self.assertEqual(b2.nbytes, 80)

            f1_loaded = b2['f1']

            self.assertEqual(b2.nbytes, 112)


    @skip_win # type: ignore
    def test_bus_dtypes_a(self) -> None:
        f1 = Frame.from_dict(
                dict(a=(1,2), b=(3,4)),
                index=('x', 'y'),
                name='f1')
        f2 = Frame.from_dict(
                dict(c=(1,2,3), b=(4,5,6)),
                index=('x', 'y', 'z'),
                name='f2')
        f3 = Frame.from_dict(
                dict(d=(10,20), b=(50,60)),
                index=('p', 'q'),
                name='f3')

        b1 = Bus.from_frames((f1, f2, f3))

        with temp_file('.zip') as fp:
            b1.to_zip_pickle(fp)
            b2 = Bus.from_zip_pickle(fp)

            self.assertEqual(b2.dtypes.to_pairs(0), ())

            f2_loaded = b2['f2']

            self.assertEqual(b2.dtypes.to_pairs(0),
                    (('c', (('f1', None), ('f2', np.dtype('int64')), ('f3', None))), ('b', (('f1', None), ('f2', np.dtype('int64')), ('f3', None))))
            )

            f3_loaded = b2['f3']

            self.assertEqual(b2.dtypes.to_pairs(0),
                    (('b', (('f1', None), ('f2', np.dtype('int64')), ('f3', np.dtype('int64')))), ('c', (('f1', None), ('f2', np.dtype('int64')), ('f3', None))), ('d', (('f1', None), ('f2', None), ('f3', np.dtype('int64')))))
                    )




    def test_bus_mloc_a(self) -> None:
        f1 = Frame.from_dict(
                dict(a=(1,2), b=(3,4)),
                index=('x', 'y'),
                name='f1')
        f2 = Frame.from_dict(
                dict(c=(1,2,3), b=(4,5,6)),
                index=('x', 'y', 'z'),
                name='f2')
        f3 = Frame.from_dict(
                dict(d=(10,20), b=(50,60)),
                index=('p', 'q'),
                name='f3')

        b1 = Bus.from_frames((f1, f2, f3))

        with temp_file('.zip') as fp:
            b1.to_zip_pickle(fp)
            b2 = Bus.from_zip_pickle(fp)

            f2_loaded = b2['f2']

            mloc1 = b2.mloc

            f3_loaded = b2['f3']
            f1_loaded = b2['f1']

            self.assertEqual(mloc1['f2'], b2.mloc.loc['f2'])


if __name__ == '__main__':
    unittest.main()
