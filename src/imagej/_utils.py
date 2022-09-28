from functools import lru_cache
from typing import Callable

from jpype import JArray, JClass, JObject
from scyjava import jimport, jvm_started

# Import Java resources on demand.


@lru_cache(maxsize=None)
def JObjectArray():
    return JArray(JObject)


class JavaClasses(object):
    """
    Utility class used to make importing frequently-used Java classes
    significantly easier and more readable.
    Benefits:
    * Minimal boilerplate
    * Lazy evaluation
    * Usable within type hints
    """

    def blocking_import(func: Callable[[], str]) -> Callable[[], JClass]:
        """
        A decorator used to lazily evaluate a java import.
        func is a function of a Python class that takes no arguments and
        returns a string identifying a Java class by name.

        Using that function, this decorator creates a property
        that when called:
        * Blocks until the ImageJ gateway has been created
        * Imports the class identified by the function
        """

        @property
        def inner(self):
            if not jvm_started():
                raise Exception()
            try:
                return jimport(func(self))
            except TypeError:
                return None

        return inner

    @blocking_import
    def Axis(self):
        return "net.imagej.axis.Axis"

    @blocking_import
    def AxisType(self):
        return "net.imagej.axis.AxisType"

    @blocking_import
    def CalibratedAxis(self):
        return "net.imagej.axis.CalibratedAxis"

    @blocking_import
    def ImagePlus(self):
        return "ij.ImagePlus"

    @blocking_import
    def Dataset(self):
        return "net.imagej.Dataset"

    @blocking_import
    def ImgPlus(self):
        return "net.imagej.ImgPlus"

    @blocking_import
    def RandomAccessibleInterval(self):
        return "net.imglib2.RandomAccessibleInterval"

    @blocking_import
    def ImgMath(self):
        return "net.imglib2.algorithm.math.ImgMath"

    @blocking_import
    def Img(self):
        return "net.imglib2.img.Img"

    @blocking_import
    def ImgView(self):
        return "net.imglib2.img.ImgView"

    @blocking_import
    def ImgLabeling(self):
        return "net.imglib2.roi.labeling.ImgLabeling"

    @blocking_import
    def Views(self):
        return "net.imglib2.view.Views"


jc = JavaClasses()
