// assets
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import TroubleshootIcon from '@mui/icons-material/Troubleshoot';
// constant
const icons = {
  QueryStatsIcon,TroubleshootIcon
};

// ==============================|| EXTRA PAGES MENU ITEMS ||============================== //

const post_modeling = {
  id: 'Post Modeling Explainability',
  title: 'Post Modeling',
  type: 'group',
  breadcrumbs: false,
  children: [
    {
      id: 'Model Prediction',
      title: 'Model Prediction',
      type: 'collapse',
      url:'/model_prediction',
      icon: icons.QueryStatsIcon,  
      children: [
        {
          id: 'Pretrained Models',
          title: 'Pretrained Models',
          type: 'item',
          url: '/pretrained_models'
        },
        {
          id: 'Custom Models',
          title: 'Custom Models',
          type: 'item',
          url: '/custom_models'
        }
      ]   
    },{
      id: 'Model Drift Detection',
      title: 'Model Drift Detection ',
      type: 'item',
      url:'/model_drift',
      icon: icons.TroubleshootIcon,  
        
    }
  ]
};

export default post_modeling;
