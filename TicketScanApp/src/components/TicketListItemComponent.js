import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Text } from 'react-native';
import { ListItem, Icon } from 'react-native-elements';
import { iOSUIKit, iOSColors } from 'react-native-typography';
import moment from 'moment/min/moment-with-locales';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';
import { styleDebug } from '../helpers';
import { systemWeights } from 'react-native-typography'

moment.locale('es');

export default function ProductListItemComponent(props) {

  const getPaymentMethodIcon = method => {
    let IconComponent;
    let name;
    let type;
    let color;
    switch (method) {
      case 'CASH':
        return <FontAwesome5
          name='coins'
          style={{ marginLeft: 10 }}
          color={iOSColors.yellow}
          size={15}
        />
      case 'CARD':
        return <Icon
          type='entypo'
          name='credit-card'
          iconStyle={{ marginLeft: 10 }}
          color={iOSColors.blue}
          size={18}
        />
      default:
        return <Icon />
    }
  };

  return (
    <ListItem
      containerStyle={styles.container}
      contentContainerStyle={styles.container}
      title={
        <View style={[styles.titleContainerStyle, { ...styleDebug('red') }]}>
          <Text style={[styles.companyName, styles.titleTextStyle]}>{props.companyName}</Text>
          <View style={{ flexDirection: 'row' }}>
            <Icon iconStyle={{ marginHorizontal: 10 }} type="ionicon" name="ios-star" color={iOSColors.yellow} size={15} />
            <Icon iconStyle={{ marginHorizontal: 10 }} type="ionicon" name="ios-flag" color={iOSColors.orange} size={15} />
          </View>
        </View>
      }
      // titleStyle={[styles.titleStyle, { ...styleDebug('red') }]}
      subtitle={
        <View style={[styles.subTitleStyle, { ...styleDebug('red') }]}>
          <Text style={[styles.subTitleTextStyle, styles.dateTextStyle]}>{moment(props.date).format('L')}</Text>
          <View style={styles.paymentInfoContainer}>
            <Text style={[styles.subTitleTextStyle, styles.paymentTextStyle]}>30,59</Text>
            {getPaymentMethodIcon('CASH')}
          </View>
        </View>
      }
      subtitleStyle={[iOSUIKit.footnote, { ...styleDebug('darkgreen') }]}
      leftIcon={
        <View style={styles.leftIconContainer}>
          <Icon type="ionicon" name="ios-star" color={iOSColors.yellow} size={15} />
          <Icon type="ionicon" name="ios-flag" color={iOSColors.orange} size={15} />
        </View>
      }
      // rightIcon={<Icon type="ionicon" name="ios-star" color={iOSColors.yellow} size={15} />}
      // leftElement={<Icon type="ionicon" name="ios-star" color='blue' size={15} />}
      // rightElement={<Icon type="ionicon" name="ios-star" color='red' size={15} />}
      leftAvatar={{ source: { uri: 'https://pbs.twimg.com/profile_images/899390660440199169/reHRnc5T_400x400.jpg' } }}
      bottomDivider={props.bottomDivider}
      topDivider={props.topDivider}
      onPress={props.onPress}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    // backgroundColor: 'transparent',
    ...styleDebug('blue'),
    justifyContent: 'space-between',
    marginLeft: 0,
    paddingVertical: 10,
    paddingRight: 10,
    height: 60,
  },
  leftIconContainer: {
    ...styleDebug('red'),
    height: 60,
    marginTop: 20,
    marginLeft: 5,
    marginRight: -10,
    paddingRight: 0,
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  icon: {

  },
  titleContainerStyle: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  titleTextStyle: {
    fontSize: 17,
  },
  companyName: {
  },
  dateTextStyle: {
    alignSelf: 'center',
  },
  paymentInfoContainer: {
    flexDirection: 'row',
  },
  paymentTextStyle: {
    alignItems: 'center',
  },
  subTitleStyle: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  subTitleTextStyle: {
    ...systemWeights.thin,
  },
});

ProductListItemComponent.propTypes = {
  companyName: PropTypes.string.isRequired,
  date: PropTypes.instanceOf(Date).isRequired,
  weight: PropTypes.string,
  weightPrice: PropTypes.string,
  leftIcon: PropTypes.node,
  bottomDivider: PropTypes.bool,
  topDivider: PropTypes.bool,
};
ProductListItemComponent.defaultProps = {
  weight: '',
  weightPrice: '',
  leftIcon: null,
  bottomDivider: false,
  topDivider: false,
};
