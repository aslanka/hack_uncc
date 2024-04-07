import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet, FlatList, Image, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: `https://${process.env.EXPO_PUBLIC_API_LOGIN_API}`,
});

const MainScreen = ({ navigation }) => {
  const [selectedTab, setSelectedTab] = useState('forYou');
  const [challenges, setChallenges] = useState([]);
  const [currentUserEmail, setCurrentUserEmail] = useState('');

  useEffect(() => {
    getCurrentUserEmail();
  }, []);

  useEffect(() => {
    if (currentUserEmail) {
      fetchChallenges();
    }
  }, [currentUserEmail, selectedTab]);

  const getCurrentUserEmail = async () => {
    try {
      const email = await AsyncStorage.getItem('userEmail');
      setCurrentUserEmail(email);
    } catch (error) {
      console.error('Error getting current user email:', error);
    }
  };

  const fetchChallenges = async () => {
    try {
      const response = await api.get('/challenges', {
        params: {
          email: currentUserEmail,
          type: selectedTab,
        },
      });
      setChallenges(response.data.challenges);
    } catch (error) {
      console.error('Error fetching challenges:', error);
    }
  };

  const handleSubscribe = async (challengeId) => {
    try {
      await api.post('/subscribe_challenge', {
        email: currentUserEmail,
        challengeId: challengeId,
      });
      fetchChallenges();
    } catch (error) {
      console.error('Error subscribing to challenge:', error);
    }
  };

  const renderChallengeItem = ({ item }) => (
    <View style={styles.challenge}>
      <Text style={styles.title}>{item.title}</Text>
      <Button
        title={item.subscribed ? 'Subscribed' : 'Subscribe'}
        color="#232323"
        onPress={() => handleSubscribe(item._id)}
        disabled={item.subscribed}
      />
      <Image source={{ uri: item.image }} style={styles.image} resizeMode="cover" />
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Custom Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.toggleDrawer()}>
          <Ionicons name="menu" size={24} color="white" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>LockedIn</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Friends')}>
          <Ionicons name="people" size={24} color="white" />
        </TouchableOpacity>
      </View>

      {/* Tab Toggle */}
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'forYou' && styles.selectedTab]}
          onPress={() => setSelectedTab('forYou')}
        >
          <Text style={[styles.tabText, selectedTab === 'forYou' && styles.selectedTabText]}>
            For You
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'friends' && styles.selectedTab]}
          onPress={() => setSelectedTab('friends')}
        >
          <Text style={[styles.tabText, selectedTab === 'friends' && styles.selectedTabText]}>
            Friends
          </Text>
        </TouchableOpacity>
      </View>

      {/* Main Content */}
      <FlatList
        style={styles.content}
        data={challenges}
        renderItem={renderChallengeItem}
        keyExtractor={(item) => item._id}
      />

      {/* Fixed Button */}
      <View style={styles.addButtonContainer}>
        <Button title="Post a Challenge" onPress={() => navigation.navigate('AddChallenge')} color="black" />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  content: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#000',
    paddingTop: 35,
  },
  headerTitle: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  },
  tabContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: 'black',
    paddingVertical: 10,
    paddingHorizontal: 30,
  },
  tab: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.5,
    shadowRadius: 3,
  },
  selectedTab: {
    backgroundColor: '#02fff1',
  },
  tabText: {
    color: 'white',
    fontSize: 16,
  },
  selectedTabText: {
    fontWeight: 'bold',
  },
  challenge: {
    margin: 10,
    padding: 15,
    backgroundColor: '#232323',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#424242",
  },
  title: {
    color: 'white',
    fontSize: 16,
    marginBottom: 10,
  },
  image: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    resizeMode: 'cover',
  },
  addButtonContainer: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    right: 20,
    backgroundColor: '#02fff1',
    borderRadius: 10,
    marginBottom: 30,
  },
});

export default MainScreen;
