// assets
import { IconDeviceAnalytics,IconReplace } from '@tabler/icons';

// constant
const icons = { IconDeviceAnalytics ,IconReplace};


// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const dashboard = {
  id: 'Pre Modeling Explainability',
  title: 'Pre Modeling',
  type: 'group',
  children: [
    {
      id: 'Data Undrestanding',
      title: 'Data Understanding',
      type: 'collapse',
      url:'/data_undrstanding',
      icon: icons.IconDeviceAnalytics,
      breadcrumbs: true,
      children: [
        {
          id: 'Initial Profiling',
          title: 'Initial Profiling',
          type: 'item',
          url: '/data_undrstanding/initial_profiling',
         
        }, {
          id: 'Data Analysis',
          title: 'Data Analysis',
          type: 'item',
          url: '/data_undrstanding/data_analysis',
        
        },
        {
          id: 'Single Column Profiling',
          title: 'Single Column Profiling',
          type: 'item',
          url: '/data_undrstanding/single_column_profiling',
         
        },
        {
          id: 'Multi Column Profiling',
          title: 'Multi Column Profiling',
          type: 'item',
          url: '/data_undrstanding/multi_column_profiling',
       
         
        },
        {
          id: 'Time Series Analysis',
          title: 'Time Series Analysis',
          type: 'item',
          url: '/data_undrstanding/time_series_analysis',
      
         
        },
        {
          id: 'OLAP Driven Analysis',
          title: 'OLAP Driven Analysis',
          type: 'item',
          url: '/data_undrstanding/olap_driven_analysis',
          breadcrumbs: true,
        },
      ],
    },

     {
      id: 'DataPreparation',
      title: 'Data Preparation',
      type: 'collapse',
      url:'/data_preparation',
      icon:icons.IconReplace,
      breadcrumbs: true,
      children: [
        {
          id: 'Missing Values Imputation',
          title: 'Missing Values Imputation',
          type: 'item',
          url: '/data_preparation/imputation',
         
        },
        {
          id: 'Outliers Handeling',
          title: 'Outliers Handeling',
          type: 'item',
          url: '/data_preparation/outlieres',
         
        },
        {
          id: 'Scaling',
          title: 'Scaling',
          type: 'item',
          url: '/data_preparation/scaling',
         
        },
        {
          id: 'Encoding',
          title: 'Encoding',
          type: 'item',
          url: '/data_preparation/encoding',
         
        },
        {
          id: 'Deleting duplicates',
          title: 'Deleting duplicates',
          type: 'item',
          url: '/data_preparation/deliting_duplicates',
         
        },
        {
          id: 'Time Series Transformation',
          title: 'Time Series Transformation',
          type: 'item',
          url: '/data_preparation/time_series_transformation',
         
        },
        {
          id: 'Preprocessing Traceability',
          title: 'Preprocessing Traceability',
          type: 'item',
          url: '/data_preparation/trace',
        },
        {
          id: 'Feature Selection',
          title: 'Feature Selection',
          type: 'item',
          url: '/data_preparation/feature_selection',
        },
      ]
    },
 
  ]
};


export default dashboard;
