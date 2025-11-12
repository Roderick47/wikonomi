from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from History.models import ProductHistory
from Product.models import Product
from Business.models import Business
from Location.models import Location


class TestProductHistoryModel(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.location = Location.objects.create(
            latitude=1.0,
            longitude=1.0
        )
        self.business = Business.objects.create(
            name='Test Business',
            description='Test Description',
            location=self.location,
            author=self.user
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=100.0,
            description='Test Description',
            business=self.business,
            author=self.user
        )
    
    def test_product_history_creation(self):
        """Test creating a product history record"""
        # Note: Product creation in setUp already creates 1 history via signal
        initial_count = ProductHistory.objects.count()
        
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product Updated',
            price=120.0,
            current_author='testuser',
            business='Test Business'
        )
        self.assertEqual(ProductHistory.objects.count(), initial_count + 1)
        self.assertEqual(history.name, 'Test Product Updated')
        self.assertEqual(history.price, 120.0)
    
    def test_product_history_str_representation(self):
        """Test the string representation of ProductHistory"""
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=100.0
        )
        str_repr = str(history)
        self.assertIn('Test Product', str_repr)
        self.assertIn(str(history.id), str_repr)
    
    def test_price_change_with_insufficient_history(self):
        """Test price_change returns '-' when less than 2 records"""
        # Clear any existing history created by signals
        ProductHistory.objects.all().delete()
        
        # Create only 1 history record
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=100.0
        )
        # With only 1 record, price_change should return '-'
        self.assertEqual(history.price_change(), '-')
    
    def test_price_change_with_two_records(self):
        """Test price_change calculation with two history records"""
        # First history record
        history1 = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=100.0,
            date_created=timezone.now()
        )
        
        # Second history record with price increase
        history2 = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=120.0,
            date_created=timezone.now()
        )
        
        # Price change should be 120 - 100 = 20
        price_change = history2.price_change()
        self.assertEqual(price_change, 20.0)
    
    def test_price_change_with_price_decrease(self):
        """Test price_change calculation with price decrease"""
        history1 = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=100.0
        )
        
        history2 = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=80.0
        )
        
        # Price change should be 80 - 100 = -20
        price_change = history2.price_change()
        self.assertEqual(price_change, -20.0)
    
    def test_price_change_with_null_prices(self):
        """Test price_change returns '-' when prices are null"""
        history1 = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=None
        )
        
        history2 = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=None
        )
        
        self.assertEqual(history2.price_change(), '-')
    
    def test_get_last_price_from_history(self):
        """Test get_last_price returns the most recent history price"""
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=150.0
        )
        
        last_price = history.get_last_price()
        self.assertEqual(last_price, 150.0)
    
    def test_get_last_price_falls_back_to_product_price(self):
        """Test get_last_price falls back to product price when no history"""
        # Create history without price
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=None
        )
        
        last_price = history.get_last_price()
        self.assertEqual(last_price, self.product.price)
    
    def test_product_history_with_author_change(self):
        """Test tracking author changes in history"""
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            previous_author='olduser',
            current_author='newuser',
            price=100.0
        )
        
        self.assertEqual(history.previous_author, 'olduser')
        self.assertEqual(history.current_author, 'newuser')
    
    def test_product_history_is_public_flag(self):
        """Test the is_public flag in history"""
        history = ProductHistory.objects.create(
            product=self.product,
            name='Test Product',
            price=100.0,
            is_public=False
        )
        
        self.assertFalse(history.is_public)
