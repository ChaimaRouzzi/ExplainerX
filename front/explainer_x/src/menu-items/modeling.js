// assets
import BuildIcon from '@mui/icons-material/Build';

const icons = {
  BuildIcon
};

// ==============================|| EXTRA PAGES MENU ITEMS ||============================== //

const pages = {
  id: 'Modeling',
  title: 'Modeling',
  type: 'group',
  breadcrumbs: false,
  children: [
    {
      id: 'Model Building',
      title: 'Model Building',
      type: 'collapse',
      url: '/model_building',
      icon: icons.BuildIcon,
      children: [
        {
          id: 'Internal Model Building',
          title: 'Internal Model Building',
          type: 'item',
          url: '/internal_model_building'
        },
        {
          id: 'External Model Building',
          title: 'External Model Building',
          type: 'item',
          url: '/external_model_building'
        }, 
        {
          id: 'List of Built Models',
          title: 'List of Built Models',
          type: 'item',
          url: 'models_list/'
        }

      ]
    }
  ]
};

export default pages;
