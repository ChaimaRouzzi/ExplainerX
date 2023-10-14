// assets
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import TroubleshootIcon from '@mui/icons-material/Troubleshoot';
// constant
const icons = {
  QueryStatsIcon,TroubleshootIcon
};

// ==============================|| EXTRA PAGES MENU ITEMS ||============================== //

const post_modeling_decideur = {
  id: 'Post Modeling Explainability',
  title: 'Post Modeling Explainability',
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
    }
  ]
};

export default post_modeling_decideur;
