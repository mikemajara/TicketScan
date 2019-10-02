import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Text } from 'react-native';
import Ionicons from 'react-native-vector-icons/Ionicons'
import { iOSUIKit } from 'react-native-typography';
import { styleDebug } from '../helpers';

export default function CardComponent(props) {
  return (
    <View style={[styles.container, props.containerStyle]}>
      <View style={[styles.iconContainer, props.iconContainerStyle]}>
        {props.icon}
      </View>
      <View style={[styles.titleContainer, props.titleContainerStyle]}>
        <Text style={[styles.title, props.titleStyle]}>{props.title}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
  },
  titleContainer: {
    // ...styleDebug('purple'),
    marginVertical: 10,
    marginHorizontal: 5,
  },
  title: {
    ...iOSUIKit.title3,
    fontSize: 18,
  },
  iconContainer: {
  },
});

CardComponent.propTypes = {};
CardComponent.defaultProps = {};