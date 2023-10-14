import { lazy } from 'react';

// project imports
import MainLayout from 'layout/MainLayout';
import Loadable from 'ui-component/Loadable';
import { useSelector } from 'react-redux';

// dashboard routing
const InitialProfiling = Loadable(lazy(() => import('views/initialProfiling')));
const SingleColumnProfiling = Loadable(lazy(() => import('views/singleColumnProfiling')));
const DataAnalysis = Loadable(lazy(() => import('views/dataAnalysis')));
const MultiColumnProfiling = Loadable(lazy(() => import('views/MultiColumnProfiling')));
const TimeSeriesAnalysis = Loadable(lazy(() => import('views/timeSeriesAnalysis')));
const PowerBI = Loadable(lazy(() => import('views/powerBI')));
const StepOneForm = Loadable(lazy(() => import('views/modelPrediction/EnergyConsumptionForm')));
const StepOneFormCustom = Loadable(lazy(() => import('views/customModelPrediction/EnergyConsumptionForm')));
const InternalModelBuilder = Loadable(lazy(() => import('views/modelBuilding')));
const ExternalModelBuilder = Loadable(lazy(() => import('views/externalModelBuilding')));
const ModelsList = Loadable(lazy(() => import('views/modelsList')));
const Imputation = Loadable(lazy(() => import('views/Imputaion')));
const Outlires = Loadable(lazy(() => import('views/outliers')));
const Scaling = Loadable(lazy(() => import('views/scaling')));
const Encoding = Loadable(lazy(() => import('views/encoding')));
const Deleting = Loadable(lazy(() => import('views/deleting')));
const Trace = Loadable(lazy(() => import('views/tracabilite')));
const FeatureSelection = Loadable(lazy(() => import('views/featureSelection')));
const TimeSeriesTransformation = Loadable(lazy(() => import('views/timeSeriesTransformation')));






const ModelDrift = Loadable(lazy(() => import('views/ModelDrift/ModelDriftForm')));

const SignIn = Loadable(lazy(() => import('views/login/Signin')));

const ConditionalMainLayout = ({ loggedInComponent, notLoggedInComponent }) => {
  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);
  return isLoggedIn ? loggedInComponent : notLoggedInComponent;

 
};




const MainRoutes = {

  path: '/',
  element: <ConditionalMainLayout loggedInComponent={<MainLayout/>} notLoggedInComponent={<SignIn />} />,
  children: [
      
    {
      path: '/',
      element: <InitialProfiling />
    },
    
      {path: '/data_undrstanding',
      children: [
        {
          path: 'initial_profiling',
          element: <InitialProfiling />
        },
        {
          path: 'single_column_profiling',
          element: <SingleColumnProfiling />
        },
        {
          path: 'data_analysis',
          element: <DataAnalysis />
        },
        {
          path: 'time_series_analysis',
          element: <TimeSeriesAnalysis />
        },
        {
          path: 'multi_column_profiling',
          element: <MultiColumnProfiling />
        },
        {
          path: 'olap_driven_analysis',
          element: <PowerBI />
        }
      ]
    },
    {
      path: '/',
      children: [
        {
          path: 'pretrained_models',
          element: <StepOneForm />
        },
        {
          path: 'custom_models',
          element: <StepOneFormCustom />
        }
      ]
    },
    {
      path: '/',
      children: [
        {
          path: 'internal_model_building',
          element: <InternalModelBuilder />
        },
        {
          path: 'external_model_building',
          element: <ExternalModelBuilder />
        },
        {
          path: 'models_list',
          element: <ModelsList />
        }
      ]
    },

    {
      path: '/',
      children: [
        {
          path: 'model_drift',
          element: <ModelDrift />
        },
      
      ]
    },
    {
      path: '/data_preparation',
      children: [
        {
          path: 'imputation',
          element: <Imputation />
        },
        {
          path: 'outlieres',
          element: <Outlires />
        },
        {
          path: 'scaling',
          element: <Scaling />
        },
        {
          path: 'encoding',
          element: <Encoding />
        },
        {
          path: 'deliting_duplicates',
          element: <Deleting />
        },
        {
          path: 'time_series_transformation',
          element: <TimeSeriesTransformation />
        },
        {
          path: 'trace',
          element: <Trace />
        }, 
        {
          path: 'feature_selection',
          element: <FeatureSelection />
        }
      ]
    }
  ]
};

export default MainRoutes;
