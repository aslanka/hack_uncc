import React from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';

const Onboarding = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <View style={styles.iconsContainer}>
      </View>
      <View style={styles.circle}>
      </View>
      <Text style={styles.headerText}>Welcome to LockedIn</Text>
      <Text style={styles.subHeaderText}>
        Create engaging habits with your friends and get inspired by your communty.
      </Text>
      <TouchableOpacity style={styles.getStartedButton} onPress={() => navigation.replace('Signup')}>
        <Text style={styles.getStartedButtonText}>Get Started</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.loginText}>Already have an account? Login</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#000',
    padding: 20,
  },
  iconsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '80%',
    marginBottom: 30,
  },
  icon: {
    width: 60,
    height: 60,
  },
  circle: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: '#02fff1',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  logoImage: {
    width: 100,
    height: 100,
  },
  headerText: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#FFFFFF',
  },
  subHeaderText: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 30,
    color: '#FFFFFF',
  },
  getStartedButton: {
    backgroundColor: '#02fff1',
    padding: 15,
    borderRadius: 30,
    width: '80%',
    alignItems: 'center',
    marginBottom: 20,
  },
  getStartedButtonText: {
    fontSize: 18,
    color: '#000',
    fontWeight: 'bold',
  },
  loginText: {
    color: '#FFFFFF',
    fontSize: 16,
  },
});

export default Onboarding;