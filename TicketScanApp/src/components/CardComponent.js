import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Text } from 'react-native';
import { iOSUIKit, systemWeights } from 'react-native-typography';
import { styleDebug } from '../helpers';

export default function CardComponent(props) {
  return (
    <View style={[styles.container, props.containerStyle]}>
      <View style={[styles.iconContainer, props.iconContainerStyle]}>{props.icon}</View>
      <View style={[styles.titleContainer, props.titleContainerStyle]}>
        <Text style={[styles.defaultTextStyle, props.titleTextStyle]}>{props.title}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
  },
  defaultTextStyle: {
    ...iOSUIKit.body,
    ...systemWeights.light,
  },
  titleContainer: {
    // ...styleDebug('purple'),
    marginVertical: 10,
    marginHorizontal: 5,
  },
  iconContainer: {},
});

CardComponent.propTypes = {
  titleTextStyle: PropTypes.object,
  titleContainerStyle: PropTypes.object,
  containerStyle: PropTypes.object,
  iconContainerStyle: PropTypes.object,
  title: PropTypes.string,
  icon: PropTypes.element,
};
CardComponent.defaultProps = {
  titleTextStyle: {},
  titleContainerStyle: {},
  containerStyle: {},
  iconContainerStyle: {},
  title: '',
  icon: <View />,
};
