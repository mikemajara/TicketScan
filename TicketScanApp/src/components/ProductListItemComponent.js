import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Text } from 'react-native';
import { ListItem, Icon } from 'react-native-elements';
import { iOSUIKit, iOSColors } from 'react-native-typography';
import { styleDebug } from '../helpers';


export default function ProductListItemComponent(props) {
  return (
    <ListItem
      containerStyle={styles.container}
      contentContainerStyle={styles.container}
      title={
        <View style={[styles.titleStyle, { ...styleDebug('red') }]}>
          <Text style={[styles.units, styles.titleTextStyle]}>{props.units}</Text>
          <Text style={[styles.name, styles.titleTextStyle]}>{props.name}</Text>
          <Text style={[styles.price, styles.titleTextStyle]}>{props.price}</Text>
        </View>
      }
      titleStyle={[styles.titleStyle, { ...styleDebug('red') }]}
      subtitle={
        props.weight &&
        props.weightPrice && (
          <View style={[styles.subTitleStyle, { ...styleDebug('red') }]}>
            <Text style={[styles.weight, styles.subTitleTextStyle]}>{props.weight}</Text>
            <Text style={[styles.weightPrice, styles.subTitleTextStyle]}>{props.weightPrice}</Text>
          </View>
        )
      }
      subtitleStyle={[iOSUIKit.footnote, { ...styleDebug('darkgreen') }]}
      leftIcon={<View style={styles.icon}>{props.leftIcon}</View>}
      // rightIcon={<Icon type="ionicon" name="ios-star" color={iOSColors.yellow} size={15} />}
      // leftElement={<Icon type="ionicon" name="ios-star" color='blue' size={15} />}
      // rightElement={<Icon type="ionicon" name="ios-star" color='red' size={15} />}
      bottomDivider={props.bottomDivider}
      topDivider={props.topDivider}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    // backgroundColor: 'transparent',
    ...styleDebug('blue'),
    justifyContent: 'space-between',
    padding: 10,
    height: 60,
  },
  icon: {
    ...styleDebug('red'),
    height: 60,
    marginTop: 20,
    marginRight: -15,
    paddingRight: 0,
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  titleStyle: {
    flexDirection: 'row',
  },
  titleTextStyle: {
    fontSize: 17,
  },
  units: {
  },
  name: {
    marginLeft: 20,
  },
  price: {
    marginLeft: 'auto',
  },
  weight: {
    marginLeft: 28,
  },
  weightPrice: {
    marginLeft: 20,
  },
  subTitleStyle: {
    flexDirection: 'row',
  },
});

ProductListItemComponent.propTypes = {
  units: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  price: PropTypes.string.isRequired,
  weight: PropTypes.string,
  weightPrice: PropTypes.string,
  leftIcon: PropTypes.node,
  bottomDivider: PropTypes.bool,
};
ProductListItemComponent.defaultProps = {
  weight: '',
  weightPrice: '',
  leftIcon: null,
  bottomDivider: false,
};
