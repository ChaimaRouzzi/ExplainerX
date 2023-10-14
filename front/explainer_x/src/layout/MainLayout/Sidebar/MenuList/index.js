// material-ui
import { Typography } from '@mui/material';

// project imports
import NavGroup from './NavGroup';
import menuItem from 'menu-items';
import menuItems2 from 'menu-items/index2';
import { useSelector } from 'react-redux';
// ==============================|| SIDEBAR MENU LIST ||============================== //

const MenuList = () => {
const userData = useSelector((state) => state.login.userData);
const role = userData ? userData : null;
console.log(role.role);
 
  const navItems = role.role=='data_scientist' ? menuItem.items.map((item) => {
    switch (item.type) {
      case 'group':
        return <NavGroup key={item.id} item={item} />;
      default:
        return (
          <Typography key={item.id} variant="h6" color="error" align="center">
            Menu Items Error
          </Typography>
        );
    }
  }):menuItems2.items.map((item) => {
    switch (item.type) {
      case 'group':
        return <NavGroup key={item.id} item={item} />;
      default:
        return (
          <Typography key={item.id} variant="h6" color="error" align="center">
            Menu Items Error
          </Typography>
        );
    }
  })

  return <>{navItems}</>;
};

export default MenuList;
