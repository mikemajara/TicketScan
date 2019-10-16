import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, SectionList, ActivityIndicator, Modal, FlatList } from 'react-native';
import { Button, ListItem, Icon, SearchBar } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { iOSColors, systemWeights, iOSUIKit } from 'react-native-typography';
import moment from 'moment/min/moment-with-locales';
import _ from 'lodash';
import AppleStyleSwipeableRow from './AppleStyleSwipeableRow';
import TicketListItemComponent from '../components/TicketListItemComponent';
import CompanyRepository from '../repository/CompanyRepository';
import TicketRepository from '../repository/TicketRepository';

import { styleDebug, mockupTicket, getMockupTicket } from '../helpers';
import LoadingComponent from '../components/LoadingComponent';

export default function TicketViewContainer(props) {

  const [elements, setElements] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const ticketRepository = new TicketRepository();

  const updateSearch = search => {
    setSearchText(search);
  };

  useEffect(() => {
    const fetchTickets = async () => {
      setLoading(true);
      try {
        const response = await ticketRepository.findAll();
        const sorted = _.sortBy(response, item => moment(item.datetime)).reverse();
        const grouped = _.groupBy(sorted, item => moment(item.datetime).format('MMMM, YYYY'));
        const sections = Object.keys(grouped).map(key => ({
          title: key,
          data: grouped[key],
        }));
        // TODO: REMOVE TRACE
        console.log(`${new Date().toISOString()} - TicketListViewContainer:36:elements`);
        console.log(sections);
        // ^^^^^ REMOVE TRACE

        setLoading(false);
        setElements(sections);
      } catch (error) {
        setLoading(false);
      }
    };

    fetchTickets();
  }, []);

  const handlePressedLine = async ticket => {
    // TODO: Ticket pressed disabled.
    props.navigation.navigate('TicketView', { ticket });
    // TODO: get ticket pressed
    // props.navigation.navigate('TicketView', { elements: response })
  };

  const arr2obj = arr => {
    const obj = {};
    arr.forEach((e, i) => {
      obj[`line${i}`] = e;
    });
    return obj;
  };

  const shouldHaveBottomDivider = (idx, len) => Boolean(len - idx - 1);
  const shouldHaveTopDivider = (idx, len) => !idx;

  return (
    <View style={styles.container}>
      {loading && (
        <LoadingComponent
          isLoading={loading}
          loadingText="Getting your tickets from the archive..."
        />
      )}
      <SectionList
        style={styles.list}
        sections={elements || []}
        renderSectionHeader={({ section: { title, data } }) => (
          <View style={styles.headerContainer}>
            <Text style={styles.headerText}>{title}</Text>
            <Text style={styles.headerText}>
              {`${data
                .map(e => e.paymentInformation.total)
                .reduce((a, b) => a + b)
                .toFixed(2)} €`}
            </Text>
          </View>
        )}
        contentOffset={{ y: 65 }}
        ListHeaderComponent={
          <View>
            <SearchBar
              platform="ios"
              containerStyle={{ backgroundColor: 'white' }}
              inputContainerStyle={{ backgroundColor: iOSColors.customGray }}
              placeholder="Search"
              onChangeText={updateSearch}
              value={searchText}
            />
          </View>
        }
        renderItem={({ item, index }) => {
          // console.log(item, index);
          return (
            <AppleStyleSwipeableRow
              flagContent={<Icon type="ionicon" name="ios-star" color="white" size={35} />}>
              <TicketListItemComponent
                ticket={item}
                bottomDivider={shouldHaveBottomDivider(index, elements.length)}
                topDivider={shouldHaveTopDivider(index, elements.length)}
                onPress={() => {
                  console.log('handling press');
                  handlePressedLine(item);
                }}
              />
            </AppleStyleSwipeableRow>
          );
        }}
        keyExtractor={(item, index) => item._id || index.toString()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    ...styleDebug('red'),
    flex: 1,
  },
  list: {
    ...styleDebug('lightgreen'),
  },
  headerContainer: {
    paddingRight: 15,
    paddingLeft: 10,
    paddingVertical: 5,
    backgroundColor: iOSColors.customGray,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  headerText: {
    ...styleDebug('red'),
    ...iOSUIKit.title3,
    ...systemWeights.thin,
  }
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
