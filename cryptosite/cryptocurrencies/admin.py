from django.contrib import admin

from .models import Coin, CoinData

class CoinAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Coin', {'fields': [
                            'name', 
                            'abbreviation']}),
        ('Valid', {'fields': ['valid']}),
        ('Date & Time', {'fields': ['created_date']}),
    ]
    list_display = ('name', 'created_date', 'valid')
    list_filter = ['name', 'created_date']

class CoinDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Coin', {'fields': ['coin']}),
        ('Valid', {'fields': ['valid']}),
        ('Market data', {'fields': [    
                                'price', 
                                'direct_volume', 
                                'total_volume', 
                                'top_tier_volume', 
                                'market_cap']}),
        ('Date & Time', {'fields': ['created_date']}),
    ]
    list_filter = ['coin', 'created_date']

admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinData, CoinDataAdmin)