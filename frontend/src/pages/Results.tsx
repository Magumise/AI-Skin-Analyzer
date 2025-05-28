import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Button, 
  Container, 
  Heading, 
  Text, 
  VStack, 
  HStack, 
  Image, 
  useBreakpointValue,
  Card,
  CardBody,
  CardHeader,
  CardFooter,
  SimpleGrid,
  Icon,
  Flex,
  Progress,
  Badge,
  Divider,
  useColorModeValue,
  Alert,
  AlertIcon,
  List,
  ListItem,
  ListIcon,
} from '@chakra-ui/react';
import { FaShoppingCart, FaArrowLeft, FaCheckCircle, FaExclamationTriangle, FaUserMd } from 'react-icons/fa';
import { Product, AnalysisResult } from '../types/index';
import './Results.css';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isDesktop = useBreakpointValue({ base: false, lg: true });
  
  // Get data from navigation state
  const { result, image } = location.state as { result: AnalysisResult; image: string };
  
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // If no result data, redirect to analysis page
  if (!result) {
    navigate('/analysis');
    return null;
  }
  
  // Format confidence as percentage
  const confidencePercentage = (result.confidence * 100).toFixed(2);
  
  // Determine confidence color based on percentage
  const getConfidenceColor = (percentage: number) => {
    if (percentage >= 80) return 'green';
    if (percentage >= 50) return 'yellow';
    return 'red';
  };
  
  // Check if condition is critical (low confidence or specific message)
  const isConditionCritical = () => {
    const hasMessage = result.message?.includes("consult a dermatologist");
    return parseFloat(confidencePercentage) < 50 || hasMessage;
  };
  
  // Get recommended products from the AI model
  const recommendedProducts = result.products || [];
  
  const handleProductClick = (product: Product): void => {
    // Handle product click
    console.log('Product clicked:', product);
  };
  
  return (
    <Box className="app-container">
      {/* Header */}
      <Box py={4} className="nav-header">
        <Container maxW="container.xl">
          <HStack justify="space-between" align="center">
            <Text fontSize="xl" fontWeight="bold" cursor="pointer" onClick={() => navigate('/')}>
              <span style={{ color: '#E53E3E' }}>GET</span>
              <span style={{ color: '#000000' }}>SKIN</span>
              <span style={{ color: '#E53E3E' }}>BEAUTY</span>
            </Text>
            {isDesktop && (
              <HStack spacing={8}>
                <Text cursor="pointer" onClick={() => navigate('/')}>Home</Text>
                <Text cursor="pointer">How it Works</Text>
                <Text cursor="pointer">About</Text>
                <Text cursor="pointer">Contact</Text>
              </HStack>
            )}
          </HStack>
        </Container>
      </Box>

      {/* Main Content */}
      <Box className="main-content" py={8}>
        <Container maxW="container.xl">
          <VStack spacing={8} align="stretch">
            <Box textAlign="center">
              <Heading size="xl" mb={4}>Analysis Results</Heading>
              <Text fontSize="lg" color="gray.600" maxW="800px" mx="auto">
                Here's what our AI detected in your skin image and our personalized recommendations.
              </Text>
            </Box>
            
            <Button 
              leftIcon={<Icon as={FaArrowLeft} />} 
              variant="outline" 
              colorScheme="red" 
              alignSelf="flex-start"
              onClick={() => navigate('/analysis')}
            >
              Back to Analysis
            </Button>
            
            {/* Results Card */}
            <Card 
              borderRadius="xl" 
              overflow="hidden" 
              boxShadow="lg"
              bg={cardBg}
              borderColor={borderColor}
            >
              <CardHeader bg="red.50">
                <Heading size="md">Skin Condition Analysis</Heading>
              </CardHeader>
              <CardBody>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8}>
                  {/* Image Column */}
                  <Box>
                    <Box 
                      borderRadius="lg" 
                      overflow="hidden" 
                      boxShadow="md"
                      mb={4}
                    >
                      <Image 
                        src={image} 
                        alt="Analyzed skin" 
                        width="100%" 
                        objectFit="cover"
                      />
                    </Box>
                    <Text fontSize="sm" color="gray.500" textAlign="center">
                      Your uploaded image
                    </Text>
                  </Box>
                  
                  {/* Results Column */}
                  <VStack align="start" spacing={4}>
                    <Box width="100%">
                      <HStack justify="space-between" mb={2}>
                        <Text fontWeight="bold">Detected Condition:</Text>
                        <Badge 
                          colorScheme={result.condition === "Normal" ? "green" : "red"} 
                          fontSize="md"
                          px={3}
                          py={1}
                          borderRadius="full"
                        >
                          {result.condition || 'Unknown'}
                        </Badge>
                      </HStack>
                      
                      <Text mb={4}>Confidence Level:</Text>
                      <Progress 
                        value={parseFloat(confidencePercentage)} 
                        colorScheme={getConfidenceColor(parseFloat(confidencePercentage))}
                        size="lg"
                        borderRadius="full"
                        mb={2}
                      />
                      <Text fontSize="sm" color="gray.500" textAlign="right">
                        {confidencePercentage}% confidence
                      </Text>
                    </Box>
                    
                    {result.message && (
                      <Alert 
                        status={result.message.includes("consult a dermatologist") ? "warning" : "info"} 
                        borderRadius="md"
                      >
                        <AlertIcon />
                        {result.message}
                      </Alert>
                    )}
                    
                    {isConditionCritical() && (
                      <Button
                        colorScheme="red"
                        size="md"
                        leftIcon={<Icon as={FaUserMd} />}
                        onClick={() => navigate('/consult-specialists', { 
                          state: { skinCondition: result.condition || 'Unknown' } 
                        })}
                        width="100%"
                      >
                        Consult Specialists
                      </Button>
                    )}
                  </VStack>
                </SimpleGrid>
              </CardBody>
            </Card>
            
            {/* Recommended Products Card */}
            <Card 
              borderRadius="xl" 
              overflow="hidden" 
              boxShadow="lg"
              bg={cardBg}
              borderColor={borderColor}
            >
              <CardHeader bg="red.50">
                <HStack justify="space-between" align="center">
                  <Heading size="md">Recommended Products</Heading>
                  <Button
                    as="a"
                    href="https://getskinbeauty.com/skincare/"
                    target="_blank"
                    rel="noopener noreferrer"
                    colorScheme="red"
                    size="sm"
                    leftIcon={<Icon as={FaShoppingCart} />}
                  >
                    View Our Products
                  </Button>
                </HStack>
              </CardHeader>
              <CardBody>
                {recommendedProducts.length > 0 ? (
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
                    {recommendedProducts.map((product: Product) => (
                      <Card 
                        key={product.id}
                        borderRadius="xl" 
                        overflow="hidden" 
                        boxShadow="lg"
                        bg={cardBg}
                        borderColor={borderColor}
                        transition="transform 0.3s"
                        _hover={{ transform: 'translateY(-5px)' }}
                      >
                        <Box 
                          height="200px" 
                          overflow="hidden"
                          position="relative"
                        >
                          {product.image ? (
                            <Image 
                              src={product.image} 
                              alt={product.name} 
                              width="100%" 
                              height="100%" 
                              objectFit="cover"
                              onError={(e) => {
                                const target = e.target as HTMLImageElement;
                                target.src = `https://via.placeholder.com/300x300?text=${product.name.replace(' ', '+')}`;
                              }}
                            />
                          ) : (
                            <Box
                              width="100%"
                              height="100%"
                              display="flex"
                              alignItems="center"
                              justifyContent="center"
                              bg="gray.100"
                            >
                              <Text color="gray.500">No Image Available</Text>
                            </Box>
                          )}
                        </Box>
                        <CardBody>
                          <VStack align="start" spacing={3}>
                            <Badge colorScheme="red">{product.category}</Badge>
                            <Heading size="md">{product.name}</Heading>
                            <Text color="gray.500">by {product.brand}</Text>
                            <Text fontSize="sm">{product.description}</Text>
                            <Text fontWeight="bold" fontSize="xl">${product.price}</Text>
                          </VStack>
                        </CardBody>
                        <CardFooter>
                          <Button 
                            colorScheme="red" 
                            width="100%" 
                            leftIcon={<Icon as={FaShoppingCart} />}
                            onClick={() => handleProductClick(product)}
                          >
                            Add to Cart
                          </Button>
                        </CardFooter>
                      </Card>
                    ))}
                  </SimpleGrid>
                ) : (
                  <Alert status="info" borderRadius="md">
                    <AlertIcon />
                    No specific products are recommended for your skin condition at this time.
                  </Alert>
                )}
              </CardBody>
            </Card>
            
            {/* Next Steps */}
            <Card 
              borderRadius="xl" 
              overflow="hidden" 
              boxShadow="lg"
              bg={cardBg}
              borderColor={borderColor}
              mt={4}
            >
              <CardHeader bg="red.50">
                <Heading size="md">Next Steps</Heading>
              </CardHeader>
              <CardBody>
                <VStack align="start" spacing={4}>
                  <HStack>
                    <Icon as={FaCheckCircle} color="green.500" />
                    <Text>Review the recommended products above</Text>
                  </HStack>
                  <HStack>
                    <Icon as={FaCheckCircle} color="green.500" />
                    <Text>Consider consulting with a dermatologist for professional advice</Text>
                  </HStack>
                  <HStack>
                    <Icon as={FaCheckCircle} color="green.500" />
                    <Text>Start a skincare routine with the recommended products</Text>
                  </HStack>
                  <HStack>
                    <Icon as={FaExclamationTriangle} color="orange.500" />
                    <Text>Monitor your skin condition and take follow-up photos in 2-4 weeks</Text>
                  </HStack>
                </VStack>
              </CardBody>
            </Card>
            
            <Box textAlign="center" mt={4}>
              <Button
                colorScheme="red"
                size="lg"
                onClick={() => navigate('/analysis')}
              >
                Analyze Another Image
              </Button>
            </Box>
          </VStack>
        </Container>
      </Box>
    </Box>
  );
};

export default Results; 