# Copyright (c) 2016-2021 by University of Kassel and Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.

import pytest

try:
    from julia.core import UnsupportedPythonError
except ImportError:
    UnsupportedPythonError = Exception
    
    
try:
    from julia import Main
    julia_installed = True 
except (ImportError, RuntimeError, UnsupportedPythonError) as e:
    julia_installed = False
    print(e)     



@pytest.mark.slow
@pytest.mark.skipif(julia_installed == False, reason="requires julia installation")
def test_julia_connection():
       
    try:
        import julia
    except:
        raise ImportError(
            "install pyjulia properlly to run PandaModels.jl")     
    try:
        julia.Julia()
    except:
        raise UserWarning(
            "cannot connect to julia, check pyjulia configuration")

       
@pytest.mark.slow
@pytest.mark.skipif(julia_installed == False, reason="requires julia installation")
# @pytest.mark.dependency(depends=['test_julia_connection'])
def test_pandamodels_installation():
    
    from julia import Main
    from julia import Pkg
    from julia import Base

    if Base.find_package("PandaModels"):  
        # remove PandaModels to reinstall it
        Pkg.rm("PandaModels")
        Pkg.resolve()

    else:
        print("PandaModels is not installed yet!")  
      
    Pkg.Registry.update()
    Pkg.add("PandaModels")  
    Pkg.build()
    Pkg.resolve()
    print("PandaModels is added to julia packages")

    try:
        Main.using("PandaModels")
        print("using PandaModels in its base mode!")
    except ImportError:
        raise ImportError("cannot use PandaModels in its base mode")
        
        
@pytest.mark.slow
@pytest.mark.skipif(julia_installed == False, reason="requires julia installation")
# @pytest.mark.dependency(depends=['test_julia_connection'])
def test_pandamodels_dev_mode(): 
    
    from julia import Main
    from julia import Pkg
    from julia import Base

    if Base.find_package("PandaModels"):  
        # remove PandaModels to reinstall it
        Pkg.rm("PandaModels")
        Pkg.resolve()
        
    Pkg.Registry.update()
    Pkg.add("PandaModels")  
    print("installing dev mode is a slow process!")  
    Pkg.resolve()
    Pkg.develop("PandaModels")
    # add pandamodels dependencies: slow process
    Pkg.instantiate()            
    Pkg.build()
    Pkg.resolve()
    print("dev mode of PandaModels is added to julia packages")

    try:
        Pkg.activate("PandaModels")
        Main.using("PandaModels")
        print("using PandaModels in its dev mode!")
    except ImportError:
        # assert False
        raise ImportError("cannot use PandaModels in its dev mode")
      
    # activate julia base mode
    Pkg.activate()
    Pkg.free("PandaModels")
    Pkg.resolve()

if __name__ == '__main__':
    pytest.main([__file__])

    