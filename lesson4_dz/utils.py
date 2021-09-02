import pandas as pd


def prefilter_items(data, drop_months=0, item_features=False, take_n_popular=0):
    '''
    Input:
        data: pd.DataFrame for transform.
        drop_months: int. Last months included to date.
        item_features: pd.DataFrame. Additional DataFrame for processing some filters.
        taken_n_popular:int. Number of popular items taken for our model (overs delited).
    '''
    # Уберем самые популярные товары (их и так купят).
    popularity_by_user = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity_by_user.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity_by_user[popularity_by_user['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят).
    top_notpopular = popularity_by_user[popularity_by_user['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев.
    if drop_months:
        data = data[data['week_no'] >= data['week_no'].max() - drop_months]

    # Уберем не интересные для рекоммендаций категории (department).
    
    
    # уберем непопулярные товары не входящие в take_n_popular.
    if take_n_popular:
        popularity_by_quantity = data.groupby('item_id')['quantity'].sum().reset_index()
        popularity_by_quantity.rename(columns={'quantity': 'n_sold'}, inplace=True)
        top = popularity_by_quantity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
        data.loc[~data['item_id'].isin(top), 'item_id'] = 99999999
        # data = data[data['item_id'] != 99999999]
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.

    
    # Уберем слишком дорогие товары
    
    # ...
    return data