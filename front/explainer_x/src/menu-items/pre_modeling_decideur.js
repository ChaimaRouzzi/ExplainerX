// assets
import { IconDeviceAnalytics,IconReplace } from '@tabler/icons';

// constant
const icons = { IconDeviceAnalytics ,IconReplace};


// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const pre_modeling_decideur = {
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
          id: 'Preprocessing Traceability',
          title: 'Preprocessing Traceability',
          type: 'item',
          url: '/data_preparation/trace',
        },
        
      ]
    },
 
  ]
};


export default pre_modeling_decideur;
